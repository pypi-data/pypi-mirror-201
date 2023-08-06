# MODULES
import enum, re, itertools, typing, datetime
import numpy as np
from collections.abc import Iterable
from typing import List
from dataclasses import fields
from time import sleep
import logging

# SQLALCHEMY
from sqlalchemy import MetaData
from sqlalchemy import inspect as inspect_sqlalchemy
import sqlalchemy
from sqlalchemy.orm import (
    RelationshipProperty,
    ColumnProperty,
)
from sqlalchemy import desc, asc
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import or_, and_, all_
from sqlalchemy.sql.elements import BinaryExpression, Null
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql.elements import Null

from flask_sqlalchemy import DefaultMeta, SQLAlchemy, BaseQuery

# MODELS
from ...models.logger import AlphaLogger
from ...models.main import AlphaException
from ...models.main._enum import MappingMode
from ...models.database.models import AlphaTable

# LIBS
from ...libs import dict_lib, py_lib

# LOCAL
from .row import Row
from .utils import get_schema
from .operators import Operators


def convert_value(value):
    if type(value) == str and len(value) > 7 and value[4] == "/" and value[7] == "/":
        return datetime.datetime.strptime(value, "%Y/%m/%d")
    if value == "now()":
        return datetime.datetime.now()
    return value


def default_return(
    results,
    default=None,
    columns: dict = None,
    page: int = None,
    per_page: int = None,
    full_count: int = None,
    first: bool = False,
    pagination_mode: str = "raw",
):
    results = results if results is not None else default
    columns = (
        {}
        if columns is None
        else {x if not hasattr(x, "key") else x.key(): y for x, y in columns.items()}
    )

    if columns is not None and type(columns) == dict:
        if type(results) == dict:
            results = {
                x if x not in columns else columns[x]: y for x, y in results.items()
            }
        elif type(results) == list and len(results) != 0 and type(results)[0] == dict:
            results = [
                {x if x not in columns else columns[x]: y for x, y in r.items()}
                for r in results
            ]

    if first and type(results) == dict and len(results) == 0:
        return None
    if page is not None and per_page is not None and pagination_mode == "raw":
        return (results, full_count)
    return results


def get_conditions_from_dict(values: dict, model=None, optional: bool = False):
    conditions = []
    for key, value in values.items():
        if type(key) == str and model is not None:
            key = getattr(model, key)

        if type(value) == set:
            value = list(value)
        elif type(value) == dict:
            for k, v in value.items():
                if issubclass(type(v), enum.Enum):
                    v = v.value
                if optional and v is None:
                    continue

                if Operators.EQUAL.equals(k) or Operators.ASIGN.equals(k):
                    conditions.append(key == v)
                elif Operators.DIFFERENT.equals(k) or Operators.NOT.equals(k):
                    conditions.append(key != v)
                elif Operators.LIKE.equals(k):
                    if not isinstance(v, Null):
                        conditions.append(key.like(v))
                    else:
                        conditions.append(key == v)
                elif Operators.NOT_LIKE.equals(k):
                    if not isinstance(v, Null):
                        conditions.append(~key.like(v))
                    else:
                        conditions.append(key != v)
                elif Operators.ILIKE.equals(k):
                    if not isinstance(v, Null):
                        conditions.append(key.ilike(v))
                    else:
                        conditions.append(key == v)
                elif Operators.NOT_ILIKE.equals(k):
                    if not isinstance(v, Null):
                        conditions.append(~key.ilike(v))
                    else:
                        conditions.append(key != v)
                elif Operators.BETWEEN.equals(k):
                    if len(v) != 2:
                        continue
                    if v[0] is not None:
                        conditions.append(key > v[0])
                    if v[1] is not None:
                        conditions.append(key < v[1])
                elif Operators.BETWEEN_OR_EQUAL.equals(k):
                    if len(v) != 2:
                        continue
                    if v[0] is not None:
                        conditions.append(key >= v[0])
                    if v[1] is not None:
                        conditions.append(key <= v[1])
                elif Operators.SUPERIOR.equals(k):
                    conditions.append(key > v)
                elif Operators.INFERIOR.equals(k):
                    conditions.append(key < v)
                elif Operators.SUPERIOR_OR_EQUAL.equals(k):
                    conditions.append(key >= v)
                elif Operators.INFERIOR_OR_EQUAL.equals(k):
                    conditions.append(key <= v)
                elif Operators.NOT_IN.equals(k):
                    v = v if isinstance(v, Iterable) else [v]
                    conditions.append(
                        key.notin_(
                            [v.value for v in v]
                            if all([issubclass(type(v), enum.Enum) for v in v])
                            else v
                        )
                    )
                elif Operators.IN.equals(k):
                    v = v if isinstance(v, Iterable) else [v]
                    conditions.append(
                        key.in_(
                            [v.value for v in v]
                            if all([issubclass(type(v), enum.Enum) for v in v])
                            else v
                        )
                    )
                elif Operators.HAS.equals(k):
                    v = get_filters(v, None, optional=optional)
                    for condition in v:
                        conditions.append(key.has(condition))
                elif Operators.ANY.equals(k):
                    v = get_filters(v, None, optional=optional)
                    conditions.append(key.any(*v))
        elif type(value) == list and value is not None:
            conditions.append(key.in_(value))
        elif not (optional and value is None):
            conditions.append(key == value)
    return conditions


def get_filters(filters, model=None, optional: bool = False):
    if filters is None:
        return []
    if type(filters) == set:
        filters = list(filters)
    elif type(filters) == dict:
        filters = [{x: y} for x, y in filters.items()]

    if type(filters) == dict:
        filters = get_conditions_from_dict(filters, model, optional=optional)
    elif type(filters) != list:
        filters = [filters]

    conditions = []
    for filter_c in filters:
        if type(filter_c) == dict:
            conditions_from_dict = get_conditions_from_dict(
                filter_c, model, optional=optional
            )
            conditions.extend(conditions_from_dict)
        elif not optional or (
            optional
            and _not_null_sqlaclhemy(filter_c.right)
            and _not_null_sqlaclhemy(filter_c.left)
        ):
            conditions.append(filter_c)

    return conditions


def get_compiled_query(query):
    if hasattr(query, "statement"):
        try:
            full_query_str = query.statement.compile(
                compile_kwargs={"literal_binds": True}
            )
        except:
            return "Failed to get query structure"
    elif hasattr(query, "query"):
        full_query_str = query.query.statement.compile(
            compile_kwargs={"literal_binds": True}
        )
    else:
        full_query_str = str(query)
    full_query_str = (
        full_query_str
        if not hasattr(full_query_str, "string")
        else full_query_str.string
    )
    return full_query_str


def add_own_encoders(conn, cursor, query, *args):
    if hasattr(cursor.connection, "encoders"):
        cursor.connection.encoders[np.float64] = lambda value, encoders: float(value)
        cursor.connection.encoders[np.int64] = lambda value, encoders: int(value)


def apply_jonctions(model, order_by):
    query = model.query
    if order_by is None:
        return query
    if type(order_by) != list and type(order_by) != tuple:
        order_by = [order_by]
    for item in order_by:
        if type(item) != str:
            item = item.key
        if item is None:
            continue
        for rel in inspect_sqlalchemy(model).relationships:
            if "." in item:
                item = item.split(".")[0]
            if item in rel.key:
                to_join = model.__dict__[item]
                if (
                    type(to_join) == InstrumentedAttribute
                    and type(to_join.prop) == RelationshipProperty
                ):
                    query = query.outerjoin(to_join)
                elif type(to_join) == InstrumentedAttribute:
                    pass  # TODO: do something ?
                elif type(to_join) == RelationshipProperty:
                    pass  # TODO: do something ?
    return query


class RetryingQuery(BaseQuery):

    __retry_count__ = 3
    __retry_sleep_interval_sec__ = 0.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        attempts = 0
        while True:
            attempts += 1
            try:
                return super().__iter__()
            except OperationalError as ex:
                if "Lost connection to MySQL server during query" not in str(ex):
                    print(">> Retry failed")
                    raise
                if attempts < self.__retry_count__:
                    print(">>Retry")
                    logging.debug(
                        "MySQL connection lost - sleeping for %.2f sec and will retry (attempt #%d)",
                        self.__retry_sleep_interval_sec__,
                        attempts,
                    )
                    sleep(self.__retry_sleep_interval_sec__)
                    continue
                else:
                    raise


def convert_order_by_str(model, order_by: str, order_by_direction: str = None):
    if model is None and order_by is not None and order_by_direction is not None:
        order_by = sqlalchemy.text(f"{order_by} {order_by_direction}")
    elif type(order_by) == str and order_by_direction is not None:
        relation = order_by
        if "." in order_by:
            order_by_split = order_by.split(".")
            relation = order_by_split[0]
            order_by = order_by_split[1]

        column = model.__dict__[relation]

        if isinstance(column.prop, RelationshipProperty):
            relation = next(
                iter(
                    [
                        rel
                        for rel in inspect_sqlalchemy(model).relationships
                        if relation in rel.key
                    ]
                ),
                None,
            )

            column = relation.mapper.class_.__dict__[order_by]

        order_by = (
            column.asc() if "asc" in order_by_direction.lower() else column.desc()
        )
    elif order_by_direction is not None:
        if hasattr(order_by, "asc"):
            order_by = (
                order_by.asc()
                if "asc" in order_by_direction.lower()
                else order_by.desc()
            )
        else:
            order_by = (
                asc(order_by) if "asc" in order_by_direction.lower() else desc(order_by)
            )
    return order_by


def apply_order_by(query, order_by, order_by_direction, model):
    if order_by is None:
        return query

    if type(order_by) != tuple and type(order_by) != list:
        query = query.order_by(
            convert_order_by_str(model, order_by, order_by_direction)
        )
    else:
        if order_by_direction is not None and len(order_by) == len(order_by_direction):
            order_by_list = [
                convert_order_by_str(model, x, y)
                for x, y in itertools.zip_longest(order_by, order_by_direction)
            ]
        elif order_by_direction is not None and type(order_by_direction) == str:
            order_by_list = [
                convert_order_by_str(model, x, order_by_direction) for x in order_by
            ]
        else:
            order_by_list = [convert_order_by_str(model, x) for x in order_by]
        query = query.order_by(*order_by_list)
    return query


class BaseModel:
    query_class = RetryingQuery


def _not_null_sqlaclhemy(element):
    return str(element).upper() != "NULL"


class AlphaDatabaseCore(SQLAlchemy):
    def __init__(
        self,
        *args,
        name: str = None,
        log: AlphaLogger = None,
        config=None,
        timeout: int = None,
        main: bool = False,
        **kwargs,
    ):
        self.db_type: str = config.get("type", "oracle")
        # cnx = config["cnx"]

        """if type(cnx) == dict:
            cnx = py_lib.filter_kwargs(create_engine, kwargs=cnx)"""
        # engine = create_engine(cnx)
        # event.listen(engine, "before_cursor_execute", add_own_encoders)
        # self._engine = engine

        engine_options = config.get("engine_options", {})
        session_options = config.get("session_options", {})
        self.autocommit = (
            "autocommit" in session_options and session_options["autocommit"]
        )
        super().__init__(
            *args,
            engine_options=engine_options,
            session_options=session_options,
            **kwargs,
        )

        """if not bind:
            session = scoped_session(sessionmaker(autocommit=False,
                                    autoflush=False,
                                    bind=engine))
            self._engine = engine
            self.Model = declarative_base()
            self.Model.query = session.query_property()
            self._session = session"""

        self.name: str = name
        self.main = main

        self.config = config
        self.log: AlphaLogger = log

        self.error = None

        self.query_str = None
        self.full_count = None
        self.pagination_mode = config.get("pagination_mode", "raw")
        self.mapping_mode = config.get("mapping_mode", MappingMode.AUTO1.value)

        self.models = []

    """def get_engine(self, bind=None):
        return self.db.get_engine(bind=self.name)

    def get_session(self):
        return self.db.session"""

    def to_json(self):
        return py_lib.get_attributes(self)

    def test(self, bind: str = None, close=False):
        """[Test the connection]

        Returns:
            [type]: [description]
        """
        engine = self.get_engine(bind=bind)
        output = False
        query = "SELECT 1"
        if self.db_type == "oracle" and not "sql" in str(engine):
            query = "SELECT 1 from dual"

        try:
            engine.execute(query)
            if not self.autocommit:
                self.session.commit()
            output = True
        except Exception as ex:
            if self.log:
                self.log.error("ex:", ex=ex)
            if not self.autocommit:
                self.session.rollback()
        finally:
            if close:
                self.session.close()
        return output

    def _get_filtered_query(
        self,
        model,
        query=None,
        filters=None,
        optional_filters=None,
        columns=None,
        likes=None,
        sup=None,
    ):

        if query is None:
            query = model.query

        if columns is not None:
            if type(columns) != list and type(columns) != List:
                columns = [columns]
            ccs = []
            for column in columns:
                """if type(column) != str:
                    ccs.append(column.key)
                else:
                    ccs.append(column)"""
                if type(column) == str and hasattr(model, column):
                    ccs.append(getattr(model, column))
                else:
                    ccs.append(column)
            query = query.with_entities(*ccs)
            # query = query.options(load_only(*columns))
            # query = query.add_columns(*ccs)

        filters = get_filters(filters, model)
        optional_filters = get_filters(optional_filters, model, optional=True)
        filters = filters + optional_filters

        if filters is not None and len(filters) != 0:
            query = query.filter(and_(*filters))
        return query


class AlphaDatabase(AlphaDatabaseCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def drop(self, table_model):
        table_model.__table__.drop(self.get_engine())

    def truncate(self, table_model, bind=None):
        if bind is None:
            bind = table_model.__bind_key__

        engine = self.get_engine(bind=bind)

        if self.db_type == "oracle" and not "sql" in str(engine):
            self.execute(f"truncate table {table_model.__tablename__}", bind=bind)
            if self.db_type == "oracle":
                try:
                    self.execute(
                        f"ALTER TABLE {table_model.__tablename__} MODIFY(ID Generated as Identity (START WITH 1));"
                    )
                except:
                    # TODO: modify
                    pass
        else:
            table_model.query.delete()
            self.commit()

    def execute(self, query, values=None, commit=True, bind: str = None, close=False):
        return self.execute_query(query, values, commit=commit, bind=bind, close=close)

    def execute_many_query(
        self, query, values=None, commit=True, bind: str = None, close=False
    ):
        return self.execute_query(query, values, multi=True, bind=bind, commit=commit)

    def execute_query(
        self,
        query,
        values={},
        multi: bool = False,
        commit: bool = True,
        bind: str = None,
        close: bool = False,
    ) -> bool:
        if self.db_type == "sqlite":
            query = query.replace("%s", "?")

        # redirect to get if select
        select = query.strip().upper()[:6] == "SELECT"
        if select:
            return self.get_query_results(
                query, values, unique=False, bind=bind, close=close
            )
        try:
            if multi:
                for value in values:
                    if value is not None:
                        self.get_engine(bind=bind).execute(query, value)
                    self.get_engine(bind=bind).execute(query)
            else:
                if values is not None:
                    self.get_engine(bind=bind).execute(query, values)
                else:
                    self.get_engine(bind=bind).execute(query)
            self.query_str = get_compiled_query(query).replace("\n", "")
            if commit and not self.autocommit:
                self.commit()
            if close:
                self.session.close()
            return True
        except Exception as ex:
            self.log.error(ex)
            raise ex

    def get(self, query, values=None, unique=False, bind: str = None, log=None):
        return self.get_query_results(
            query, values=values, unique=unique, bind=bind, log=log
        )

    def get_query_results(
        self,
        query,
        values=None,
        unique=False,
        log=None,
        bind=None,
        close=False,
        dataclass=None,
    ):
        session = self.get_engine(self.app, bind)

        if self.db_type == "sqlite":
            query = query.replace("%s", "?")

        if log is None:
            log = self.log

        if values is not None:
            if type(values) == list and len(values) != 0:
                dict_values = {}
                for i, val in enumerate(values):
                    if type(val) == dict:
                        query = query.replace(":%s" % list(val.keys())[0], f":p{i}", 1)
                        dict_values[f"p{i}"] = list(val.values())[0]
                    else:
                        query = query.replace("?", f":p{i}", 1)
                        dict_values[f"p{i}"] = val
                values = dict_values

        try:
            resultproxy = (
                session.execute(query, values)
                if values is not None
                else session.execute(query)
            )
        except Exception as ex:
            if log is not None:
                log.error(ex)
            raise ex

        results = []
        for rowproxy in resultproxy:
            if hasattr(rowproxy, "items"):
                columns = {column: value for column, value in rowproxy.items()}
            else:
                columns = [x for x in rowproxy]
            results.append(columns)

        if not unique:
            if dataclass is None:
                rows = [Row(x) for x in results]
            else:
                rows = [dataclass(**x) for x in results]
        else:
            rows = [
                value[0] if not hasattr(value, "keys") else list(value.values())[0]
                for value in results
            ]
        self.query_str = get_compiled_query(query).replace("\n", "")

        """
        except Exception as err:
            stack = inspect.stack()
            parentframe = stack[1]
            module = inspect.getmodule(parentframe[0])
            root = os.path.abspath(module.__file__).replace(module.__file__, "")
            error_message = "In file {} line {}:\n {} \n\n {}".format(
                parentframe.filename,
                parentframe.lineno,
                "\n".join(parentframe.code_context),
                err,
            )
            if self.log is not None:
                self.log.error(error_message)
        """
        if close:
            session.close()

        return rows

    def get_blocked_queries(self, bind: str = None):
        query = """SELECT SQL_TEXT
        FROM performance_schema.events_statements_history ESH,
            performance_schema.threads T
        WHERE ESH.THREAD_ID = T.THREAD_ID
        AND ESH.SQL_TEXT IS NOT NULL
        AND T.PROCESSLIST_ID = %s
        ORDER BY ESH.EVENT_ID LIMIT 10;"""

        transaction_id = None
        result_list = self.get_engine().execute("show engine innodb status;")
        outputs = {}
        for result in list(result_list)[0]:
            for line in result.split("\n"):
                if transaction_id is not None:
                    matchs_thread = re.findall("thread id ([0-9]*),", line)
                    matchs_query = re.findall("query id ([0-9]*)", line)
                    if len(matchs_thread):
                        trs = self.get_query_results(
                            query % matchs_thread[0], bind=bind
                        )
                        outputs[int(times)] = [x["SQL_TEXT"] for x in trs]
                    transaction_id = None

                matchs_tr = re.findall(
                    "---TRANSACTION ([0-9]*), ACTIVE ([0-9]*) sec", line
                )
                if len(matchs_tr) != 0:
                    transaction_id, times = matchs_tr[0]
        outputs = dict_lib.sort_dict(outputs, reverse=True)
        return outputs

    def insert(self, model, values={}, commit=True, test=False, close=False):
        values_update = self.get_values(model, values, {})
        return self.add(
            model, parameters=values_update, commit=commit, test=test, close=close
        )

    def insert_or_update(self, model, values={}, commit=True, test=False):
        # return self.upsert(model, values)
        values_update = self.get_values(model, values, {})
        return self.add(
            model, parameters=values_update, commit=commit, test=test, update=True
        )

    def values_to_model(self, model, values):
        if type(values) != dict:
            self.log.error("<values must be of type <dict>")
            return None
        values = {
            x if not "." in str(x) else str(x).split(".")[-1]: y
            for x, y in values.items()
        }
        obj = model(**values)
        return obj

    def add_or_update(self, obj, parameters=None, commit=True, test=False, update=True):
        return self.add(
            obj, parameters=parameters, commit=commit, test=test, update=True
        )

    def add(
        self,
        model,
        parameters=None,
        commit: bool = True,
        test: bool = False,
        update: bool = False,
        flush: bool = True,
        close: bool = False,
    ) -> object:
        if test:
            self.log.info(f"Insert {model} with values {parameters}")
            return None

        obj = model
        if parameters is not None:
            if type(parameters) != dict:
                self.log.error("<parameters must be of type <dict>")
                return None
            parameters = {
                x if not "." in str(x) else str(x).split(".")[-1]: y
                for x, y in parameters.items()
            }
            obj = model(**parameters)

        if type(obj) == list:
            if not update:
                self.session.add_all(obj)
            else:
                for o in obj:
                    self.session.merge(o)
        else:
            if not update:
                self.session.add(obj)
            else:
                self.session.merge(obj)

        if commit and not self.autocommit:
            self.commit()
        elif flush:
            self.session.flush()
        if close:
            self.session.close()
        return obj

    def upsert(self, model, rows, bind=None):
        if type(rows) != list:
            rows = [rows]
        from sqlalchemy.dialects import postgresql
        from sqlalchemy import UniqueConstraint

        table = model.__table__
        stmt = postgresql.insert(table)
        primary_keys = [key.name for key in inspect_sqlalchemy(table).primary_key]
        update_dict = {c.name: c for c in stmt.excluded if not c.primary_key}

        if not update_dict:
            raise ValueError("insert_or_update resulted in an empty update_dict")

        stmt = stmt.on_conflict_do_update(index_elements=primary_keys, set_=update_dict)

        seen = set()
        foreign_keys = {
            col.name: list(col.foreign_keys)[0].column
            for col in table.columns
            if col.foreign_keys
        }
        unique_constraints = [
            c for c in table.constraints if isinstance(c, UniqueConstraint)
        ]

        def handle_foreignkeys_constraints(row):
            for c_name, c_value in foreign_keys.items():
                foreign_obj = row.pop(c_value.table.name, None)
                row[c_name] = (
                    getattr(foreign_obj, c_value.name) if foreign_obj else None
                )

            for const in unique_constraints:
                unique = tuple(
                    [
                        const,
                    ]
                    + [getattr(row, col.name) for col in const.columns]
                )
                if unique in seen:
                    return None
                seen.add(unique)

            return row

        rows = list(filter(None, (handle_foreignkeys_constraints(row) for row in rows)))
        self.session.execute(stmt, rows, bind=bind)

    def commit(self, close=False, session=None):
        if self.autocommit:
            return True
        if session is None:
            session = self.session
        valid = True
        try:
            session.commit()
        except Exception as ex:
            self.log.error(ex=ex)
            session.rollback()
            raise ex

            valid = False
        finally:
            if close:
                session.close()
        return valid

    def delete_obj(self, obj, commit: bool = True, close: bool = False) -> bool:
        session = self.object_session(obj)
        session.delete(obj)
        if commit:
            return self.commit(close=close, session=session)
        return True

    def delete(self, model, filters, commit: bool = True, close: bool = False) -> bool:
        if filters is None or len(filters) == 0:
            raise AlphaException("Cannot delete without specifying filters")
        objs = self.select(model, filters=filters, json=False)
        if len(objs) == 0:
            return False
        for obj in objs:
            self.delete_obj(obj, commit=False)
        if commit:
            return self.commit(close=close)
        return True

    def get_tables_names(self, bind: str = None):
        return list(
            set(
                [
                    x.__tablename__
                    for x in self.get_tables_models(
                        binds=[bind] if bind is not None else None
                    )
                ]
            )
        )

    def get_all_binds(self):
        # TODO: add main
        return list(
            set(
                [
                    x.__bind_key__
                    for x in self.get_tables_models()
                    if getattr(x, "__bind_key__", None) is not None
                ]
            )
        )

    def get_table_model(self, table: str, bind: str = None):
        table = next(
            iter(
                self.get_tables_models(
                    tables=[table], binds=[bind] if bind is not None else None
                )
            ),
            None,
        )
        if table is None:
            raise AlphaException("cannot_find_table", parameters={"table": table})
        return table

    def get_table_columns(self, table: str):
        model = self.get_table_model(table)
        return model._sa_class_manager.local_attrs

    def get_tables_models(
        self, tables: List[str] = None, binds: List[str] = None
    ) -> list:
        if tables is not None:
            tables = [x.upper() for x in tables]
        models = self.__get_tables_models()
        registered_models = [
            x
            for x in models
            if (binds is None or getattr(x, "__bind_key__", None) in binds)
            and (tables is None or x.__tablename__.upper() in tables)
        ]
        return registered_models

    def __get_tables_models(self, force: bool = False):
        if len(self.models) == 0 or force:
            if hasattr(self.Model, "_decl_class_registry"):
                registries = self.Model._decl_class_registry
                registered_classes = [x for x in registries.values()]
                registered_models: typing.Dict[str, DefaultMeta] = [
                    x for x in registered_classes if isinstance(x, DefaultMeta)
                ]
            else:
                registered_models = [
                    x
                    for x in self.Model.registry._class_registry.values()
                    if hasattr(x, "__tablename__")
                ]
            self.models = registered_models
        return self.models

    def ensure(self, table_name: str, bind=None, drop: bool = False):
        if not table_name.lower() in self.get_bind_tablenames(bind):
            request_model = self.get_table_model(bind, table_name)

            self.log.info(f"Creating <{table_name}> table in <{bind}> database")
            try:
                request_model.__table__.create(self.get_engine(bind=bind))
            except Exception as ex:
                if drop:
                    self.log.info(f"Drop <{table_name}> table in <{bind}> database")
                    request_model.__table__.drop(self.get_engine(bind=bind))
                    self.ensure(table_name)
                else:
                    self.log.error(ex)

        """
        
        #if not cls.__tablename__ in cls.metadata.tables:
        #    cls.metadata.create_all()
        # ensure tests
        
        if not self.exist(request_model):
            self.log.info('Creating <%s> table in <%s> database'%(table_name,self.name))
            try:
                request_model.__table__.create(self.get_engine(bind=bind))
            except Exception as ex:
                if drop:
                    self.log.info('Drop <%s> table in <%s> database'%(table_name,self.name))
                    request_model.__table__.drop(self.get_engine(bind=bind))
                    self.ensure(table_name)
                else:
                    self.log.error(ex)
        """

    def exist(self, model):
        try:
            instance = self.session.query(model).first()
            return True
        except Exception as ex:
            self.log.error(ex=ex)
            return False

    def select(
        self,
        model,
        filters: list = None,
        optional_filters: list = None,
        first: bool = False,
        json: bool = False,
        unique: InstrumentedAttribute = None,
        count: bool = False,
        order_by=None,
        order_by_direction=None,
        group_by=None,
        distinct=None,
        limit: int = None,
        columns: list | dict = None,
        close=False,
        flush=False,
        schema=None,
        relationship=True,
        disabled_relationships: typing.List[str] = None,
        page: int = None,
        per_page: int = None,
        offset: int = None,
        dataclass=None,
        default=None,
    ):
        query = apply_jonctions(model, order_by)

        # model_name = inspect.getmro(model)[0].__name__
        # if self.db_type == "mysql": self.test(close=False)
        renames_columns = None
        if type(columns) == dict:
            columns = list(columns.keys())
            renames_columns = columns

        if columns is not None and (
            len(columns) == 0 or len([x for x in columns if str(x) != ""]) == 0
        ):
            columns = None

        attributes = {}
        for key, col in dict(model.__dict__).items():
            if not hasattr(col, "prop"):
                continue

            binary_expression = type(col.expression) is BinaryExpression
            column_property = isinstance(col.prop, ColumnProperty)

            if not relationship and (column_property and not binary_expression):
                attributes[key] = col

            #! TOTO: modify
            """if disabled_relationships:
                if (column_property or isinstance(col.prop, RelationshipProperty)) and not binary_expression and key not in disabled_relationships:
                    attributes[key] = col"""

        if len(attributes) != 0:
            columns = (
                attributes.values()
                if columns is None
                else columns.extend(attributes.values())
            )

        if unique and (
            type(unique) == InstrumentedAttribute or type(unique) == str
        ):  # TODO: upgrade
            columns = [unique]
            distinct = True
            json = True
        elif unique:
            raise AlphaException(
                "Parameter or <unique> must be of type <InstrumentedAttribute> or <str>"
            )

        query = self._get_filtered_query(
            model,
            query=query,
            filters=filters,
            optional_filters=optional_filters,
            columns=columns,
        )

        return self.select_query(
            query,
            model=model,
            first=first,
            json=json,
            unique=unique,
            count=count,
            limit=limit,
            order_by=order_by,
            order_by_direction=order_by_direction,
            close=close,
            flush=flush,
            schema=schema,
            relationship=relationship,
            disabled_relationships=disabled_relationships,
            page=page,
            per_page=per_page,
            offset=offset,
            dataclass=dataclass,
            default=default,
            columns=renames_columns,
            distinct=distinct,
            group_by=group_by,
        )

    def select_query(
        self,
        query,
        model=None,
        first: bool = False,
        json: bool = False,
        unique: InstrumentedAttribute = None,
        count: bool = False,
        limit: int = None,
        filters: list = None,
        optional_filters: list = None,
        order_by=None,
        order_by_direction=None,
        close=False,
        flush=False,
        schema=None,
        relationship=True,
        disabled_relationships: typing.List[str] = None,
        page: int = None,
        per_page: int = None,
        offset: int = None,
        dataclass=None,
        default=None,
        columns: dict = None,
        distinct=None,
        group_by=None,
    ):
        if per_page is not None and page is None:
            page = 0
        if distinct is not None:
            query = (
                query.distinct(distinct)
                if type(distinct) != tuple
                else query.distinct(*distinct)
            )

        if group_by is not None:
            query = (
                query.group_by(group_by)
                if type(group_by) != tuple
                else query.group_by(*group_by)
            )

        self.full_count = None
        if dataclass is not None:
            json = True
        if filters is not None:
            filters = get_filters(filters, model=None, optional=False)
            query = query.filter(and_(*filters))
        if optional_filters is not None:
            optional_filters = get_filters(optional_filters, model=None, optional=True)
            query = query.filter(and_(*optional_filters))

        if first and limit is None:
            limit = 1

        if page is not None and per_page is not None:
            self.full_count = query.count()
            query = apply_order_by(query, order_by, order_by_direction, model)
            query = query.limit(per_page).offset(page * per_page)
        else:
            query = apply_order_by(query, order_by, order_by_direction, model)
            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)
            if count:
                results = query.count()
                self.query_str = get_compiled_query(query).replace("\n", "")
                # self.log.debug(self.query_str)
                return default_return(
                    results,
                    default=default,
                    columns=columns,
                    page=page,
                    per_page=per_page,
                    full_count=self.full_count,
                    first=first,
                    pagination_mode=self.pagination_mode,
                )

        try:
            results = query.all() if not first else query.first()
        except Exception as ex:
            compiled_query = get_compiled_query(query)
            self.query_str = compiled_query.replace("\n", "")
            self.log.error(f'non valid query "{self.query_str}"', ex=ex)
            query.session.close()
            raise ex
            # raise AlphaException('non_valid_query',get_compiled_query(query),str(ex)))
        if close:
            query.session.close()
        if flush:
            query.session.flush()
        if disabled_relationships:
            json = True
        if not json:
            self.query_str = get_compiled_query(query).replace("\n", "")
            # self.log.debug(self.query_str, level=2)
            return default_return(
                results,
                default=default,
                columns=columns,
                page=page,
                per_page=per_page,
                full_count=self.full_count,
                first=first,
                pagination_mode=self.pagination_mode,
            )
        # json conversion
        results_json = {}
        if schema is None and model is not None:
            schema = get_schema(
                model,
                relationship=relationship,
                disabled_relationships=disabled_relationships,
            )

            structures = schema(many=True) if not first else schema()
            results_json = structures.dump(results)
        elif results is not None:
            results_json = (
                (
                    results.to_json()
                    if hasattr(results, "to_json")
                    else results._asdict()
                )
                if type(results) != list
                else [
                    (x.to_json() if hasattr(x, "to_json") else x._asdict())
                    for x in results
                ]
            )

        self.query_str = get_compiled_query(query).replace("\n", "")
        # self.log.debug(self.query_str, level=2)

        if unique:
            if type(unique) == str:
                if not first:
                    return default_return(
                        (
                            []
                            if len(results_json) == 0
                            else [x[unique] for x in results_json]
                        ),
                        default=default,
                        columns=columns,
                        page=page,
                        per_page=per_page,
                        full_count=self.full_count,
                        first=first,
                        pagination_mode=self.pagination_mode,
                    )
                else:
                    return default_return(
                        (results_json[unique]),
                        default=default,
                        columns=columns,
                        page=page,
                        per_page=per_page,
                        full_count=self.full_count,
                        first=first,
                        pagination_mode=self.pagination_mode,
                    )
            else:
                if not first:
                    return default_return(
                        (
                            []
                            if len(results_json) == 0
                            else [
                                x[unique.key] for x in results_json if unique.key in x
                            ]
                        ),
                        default=default,
                        columns=columns,
                        page=page,
                        per_page=per_page,
                        full_count=self.full_count,
                        first=first,
                        pagination_mode=self.pagination_mode,
                    )
                else:
                    return default_return(
                        (
                            results_json[unique.key]
                            if unique.key in results_json
                            else None
                        ),
                        default=default,
                        columns=columns,
                        page=page,
                        per_page=per_page,
                        full_count=self.full_count,
                        first=first,
                        pagination_mode=self.pagination_mode,
                    )
        """if disabled_relationships and not json:
            if type(results_json) == dict:
                results_json = model(**results_json)
            elif type(results_json) == list:
                results_json = [model(**x) for x in results_json]"""
        if dataclass is not None:
            if len(results_json) == 0:
                return default_return(
                    [] if not first else default,
                    default=default,
                    columns=columns,
                    page=page,
                    per_page=per_page,
                    full_count=self.full_count,
                    first=first,
                    pagination_mode=self.pagination_mode,
                )

            is_alpha_dataclass = hasattr(dataclass, "auto_map_from_dict")
            mapping_mode = (
                getattr(dataclass, "__map__").lower()
                if hasattr(dataclass, "__map__")
                else self.mapping_mode.lower()
            )
            field_names = [field.name for field in fields(dataclass)]

            if not first:
                if is_alpha_dataclass:
                    results_json = [
                        dataclass.map(r, mapping_mode) for r in results_json
                    ]
                else:
                    results_json = [
                        dataclass(**{x: y for x, y in k.items() if x in field_names})
                        for k in results_json
                    ]
            else:
                if is_alpha_dataclass:
                    results_json = dataclass.map(results_json, mapping_mode)
                else:
                    results_json = dataclass(
                        **{x: y for x, y in results_json.items() if x in field_names}
                    )
        return default_return(
            results_json,
            default=default,
            columns=columns,
            page=page,
            per_page=per_page,
            full_count=self.full_count,
            first=first,
            pagination_mode=self.pagination_mode,
        )

    def update(
        self,
        model,
        values={},
        filters=None,
        fetch: bool = True,
        commit: bool = True,
        close: bool = False,
        not_none: bool = False,
    ) -> bool:
        if type(model) != list:
            state, models, values_list = inspect_sqlalchemy(model), [model], [values]
        else:
            state, models, values_list = inspect_sqlalchemy(model[0]), model, values

        is_transient = state.transient if hasattr(state, "transient") else False
        if is_transient:
            return self.__update_transient(
                models, filters=filters, commit=commit, close=close
            )

        size_values = len(values)
        for i, model in enumerate(models):
            if i < size_values:
                values = values_list[i]

            if hasattr(model, "metadata"):
                filters = [] if filters is None else filters

                attributes = model._sa_class_manager.local_attrs

                if len(filters) == 0:
                    for name, attribute in attributes.items():
                        val = None
                        if name in values:
                            val = values[name]
                        elif attribute.expression.key in values:
                            val = values[attribute.expression.key]

                        if (
                            hasattr(attribute.expression, "primary_key")
                            and attribute.expression.primary_key
                            and val is not None
                        ):
                            filters.append(attribute == val)

                filters = get_filters(filters, model)
                if len(filters) == 0:
                    self.log.error(f"Cannot find any entry for model {model}")
                    return False
                rows = self.select(model, filters=filters)
                if len(rows) == 0:
                    self.log.error(f"Cannot find any entry for model {model}")
                    return False

                for row in rows:
                    for key, value in values.items():
                        if not_none and value is None:
                            continue
                        setattr(row, key if type(key) == str else key.key, value)
                    self.session.merge(row)
            else:
                query = self._get_filtered_query(model, filters=filters)
                values_update = self.get_values(model, values, filters)

                if fetch:
                    query.update(values_update, synchronize_session="fetch")
                else:
                    try:
                        query.update(values_update, synchronize_session="evaluate")
                    except:
                        query.update(values_update, synchronize_session="fetch")

        if commit:
            return self.commit(close)
        return True

    def __update_transient(
        self,
        transients,
        filters=None,
        commit: bool = True,
        close: bool = False,
    ):
        for i, transient in enumerate(transients):
            model = transient.__class__
            filters = [] if filters is None else filters

            attributes = model._sa_class_manager.local_attrs

            if len(filters) == 0:
                for name, attribute in attributes.items():
                    val = getattr(transient, name)

                    if (
                        hasattr(attribute.expression, "primary_key")
                        and attribute.expression.primary_key
                        and val is not None
                    ):
                        filters.append(attribute == val)

            filters = get_filters(filters, model)
            if len(filters) == 0:
                self.log.error(f"Cannot find any entry to update for model {model}")
                return False
            rows = self.select(model, filters=filters)
            if len(rows) == 0:
                self.log.error(f"Cannot find any entry for model {model}")
                return False

            if len(rows) != 1:
                self.log.error(
                    f"Too much entries to update corresponding to {transient}"
                )
                return False
            self.session.merge(transient)
        if commit:
            return self.commit(close)
        return True

    def get_values(self, model, values, filters=None):
        values_update = {}
        for key, value in values.items():
            if type(key) == InstrumentedAttribute and not key in filters:
                values_update[key] = value
            elif type(key) == str and hasattr(model, key) and not key in filters:
                values_update[model.__dict__[key]] = value
        return values_update

    def process_entries(self, bind, table, values: list, headers: list = None):
        if headers is not None:
            headers = [
                x.lower().replace(" ", "_")
                if hasattr(x, "lower")
                else str(x).split(".")[1]
                for x in headers
            ]

            columns_names = {}
            for name, col in table.__dict__.items():
                if hasattr(col, "expression") and hasattr(col.expression, "name"):
                    columns_names[col.expression.name] = name

            entries = [
                table(
                    **{
                        columns_names[headers[i]]: convert_value(value)
                        for i, value in enumerate(values_list)
                        if headers[i] in columns_names
                    }
                )
                for values_list in values
            ]
        else:
            entries = values

        # db.session.query(class_instance).delete()
        # db.session.add_all(entries)
        session = self.create_scoped_session(options={"bind": bind})

        for entry in entries:
            session.merge(entry)
        session.commit()

    def init_all(
        self,
        binds: List[str] = None,
        tables: List[AlphaTable] = None,
        drop: bool = False,
        create: bool = False,
        sqlite: bool = True,
    ):
        """if sqlite:
        binds = [
            x.upper()
            for x, y in self.db_cnx.items()
            if y["type"] == "sqlite" and (binds is None or x in binds)
        ]"""

        """for bind, tables_dict in self.tables.items():
            if binds is None or bind in binds:
                for table_name, table_model in tables_dict.items():
                    engine = self.db.get_engine(bind=bind)
                    if drop:
                        table_model.__table__.drop(engine)
                    table_model.__table__.create(engine)"""
        """if drop:
            self._db.drop_all(bind=binds, tables=tables)
        self._db.create_all(bind=binds, tables=tables)"""

        tables_by_bind = {}
        for table_model in tables:
            bind = (
                "MAIN"
                if not hasattr(table_model, "__bind_key__")
                else table_model.__bind_key__
            )
            if not bind in tables_by_bind:
                tables_by_bind[bind] = [table_model]
            else:
                tables_by_bind[bind].append(table_model)

        for bind, tables_models in tables_by_bind.items():
            tables = [x.__table__ for x in tables_models]
            meta = MetaData(self.get_engine(bind=bind))
            if drop:
                meta.drop_all(tables=tables)
            meta.create_all(tables=tables)

    def create_table(self, table: str, bind: str = None, drop: bool = False):
        table_object = self.get_table_model(table, bind)
        if drop:
            try:
                table_object.__table__.drop(self.engine)
            except:
                pass
        table_object.__table__.create(self.engine)
        return True

    def drop_table(self, table: str, bind: str = None):
        table_object = self.get_table_model(table, bind)
        table_object.__table__.drop(self.db.engine)
