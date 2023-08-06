# MODULES
import glob, os, importlib, re
from typing import Dict, List

# LIBS
from . import io_lib

# MODELS
from ..models.main import AlphaException

# CORE
from core import core


def init_databases(
    core,
    tables: List[str] | Dict[str, str] = None,
    binds: List[str] = None,
    create: bool = False,
    drop: bool = False,
    truncate: bool = False,
    sqlite: bool = True,
    force: bool = True,
    init: bool = False,
):
    if core.configuration != "local" and not force:
        if core.log:
            core.log.error("Configuration must be <local>")
        return

    if tables is not None:
        tables = (
            {x.upper(): None for x in tables}
            if type(tables) == list
            else {x.upper(): y for x, y in tables.items()}
        )

    db_binds = core.db.get_all_binds()
    binds = [bind.upper() for bind in binds] if binds is not None else db_binds
    if len(binds) != len(db_binds):
        for bind in binds:
            if not bind in db_binds:
                raise AlphaException(f"Cannot find {bind=}")

    tables_models = core.db.get_tables_models(tables, binds)

    init_databases_config = core.config.get("databases")
    if init_databases_config is None:
        raise AlphaException(
            "No initialisation configuration has been set in <databases> entry"
        )
    init_databases_config = {x.upper(): y for x, y in init_databases_config.items()}

    core.db.init_all(tables=tables_models, create=create, drop=drop, sqlite=sqlite)

    if tables is not None and truncate:
        for table_model in tables_models:
            core.db.truncate(table_model)

    ini_types = {
        "json": {"key": "init_database_dir_json", "pattern": "*.json"},
        "py": {"key": "init_database_dir_py", "pattern": "*.py"},
        "sql": {"key": "init_database_dir_sql", "pattern": "*.sql"},
    }

    for bind in binds:
        if not bind in init_databases_config:
            core.log.warning(
                f"No initialisation configuration has been set in <databases> entry for {bind=}"
            )
            continue

        for ini_type, cf_ini in ini_types.items():
            bind_cf = init_databases_config[bind]
            if type(bind_cf) == str and bind_cf in init_databases_config:
                bind_cf = init_databases_config[bind_cf]
            if not cf_ini["key"] in bind_cf:
                continue

            ini_dir = bind_cf[cf_ini["key"]]
            files = glob.glob(ini_dir + os.sep + cf_ini["pattern"])

            for file_path in files:
                l_table_name = file_path.split(os.sep)[-1].split(".")[0].upper()
                if tables is not None and len(tables) != 0:
                    if not l_table_name in tables:
                        continue
                __process_databases_init(
                    core, core.db, bind, l_table_name, file_path, file_type=ini_type
                )


def __process_databases_init(core, db, bind, table_name, file_path, file_type="py"):
    if file_type == "py":
        current_path = os.getcwd()
        module_path = (
            file_path.replace(current_path, "")
            .replace("/", ".")
            .replace("\\", ".")
            .replace(".py", "")
        )

        if module_path[0] == ".":
            module_path = module_path[1:]

        module = importlib.import_module(module_path)

        if hasattr(module, "ini"):
            ini = module.__dict__["ini"]
            if type(ini) != dict:
                raise AlphaException(
                    "In file {file_path} <ini> configuration must be of type <dict>"
                    % (file_path)
                )
            for real_table_name, conf in ini.items():
                if type(real_table_name) != str and hasattr(
                    real_table_name, "__tablename__"
                ):
                    real_table_name = getattr(real_table_name, "__tablename__")
                if real_table_name.upper() == table_name.upper():
                    __get_entries(core, db, bind, table_name, file_path, conf)
    elif file_type == "json":
        try:
            ini = io_lib.read_json(file_path)
        except Exception as ex:
            raise AlphaException("Cannot read file %s: %s" % (file_path, ex))

        __get_entries(core, db, bind, table_name, file_path, ini)
    elif file_type == "sql":
        with open(file_path, "r") as f:
            sql = f.read()
            matchs = re.findall(r"to_date\('[^']+','[^']+'\)", sql)
            for match in matchs:
                date = match.replace("to_date(", "").split(",")[0]
                format = match.split(",")[1].replace(")", "")
                sql = sql.replace(match, f"strftime({format}, {date})")
            statements = sql.split(";")
            for statement in statements:
                try:
                    db.execute(statement, bind=bind.upper())
                except Exception as ex:
                    db.log.error(ex=ex)


def __get_entries(core, db, bind, table_name, file_path, configuration):
    # TODO: fix

    if type(configuration) != dict:
        core.log.error(
            f"In file {file_path} configuration of {bind=} must be of type <dict>"
        )
        return

    table = core.db.get_table_model(table_name)

    object_initiated = "objects" in configuration
    if object_initiated:
        entries = configuration["objects"]
        db.process_entries(bind, table, values=entries)
        core.log.info(f"{table_name=} and {bind=} initiated with file {file_path}")

    data_type = "alpha"
    if "headers" in configuration and "values" in configuration:
        values = configuration["values"]
        headers = configuration["headers"]
    elif (
        "results" in configuration
        and "columns" in configuration["results"][0]
        and "items" in configuration["results"][0]
    ):
        values = configuration["results"][0]["items"]
        headers = list(configuration["results"][0]["items"][0].keys())
        data_type = "sql"
    else:
        if not object_initiated:
            core.log.error(
                f"Ini configuration in file {file_path} does not have a valid structure"
            )
        return

    if type(values) != list:
        core.log.error(
            f'In file {file_path} "values" key from {table_name=} and {bind=} must be of type <list>'
        )
        return

    if type(headers) != list:
        core.log.error(
            f'In file {file_path} "headers" key from {table_name=} and {bind=} must be of type <list>'
        )
        return

    entries = []
    for entry in values:
        if type(entry) != list and data_type == "alpha":
            core.log.error(
                f"In file {file_path} from {table_name=} and {bind=} entries must be of type <list>"
            )
            continue
        elif type(entry) != dict and data_type == "sql":
            core.log.error(
                f"In file {file_path} from {table_name=} and {bind=} entries must be of type <dict>"
            )
            continue
        entries.append(entry if data_type == "alpha" else list(entry.values()))

        """if LOG:
            LOG.info(
                "Adding %s entries from <list> for {table_name=} in {bind=} from file %s"
                % (len(entries), table_name, database, file_path)
            )"""
    db.process_entries(bind, table, headers=headers, values=entries)
    core.log.info(f"{table_name=} and {bind=} initiated with file {file_path}")


def get_table_content(
    bind: str,
    tablename: str,
    order_by: str,
    direction: str,
    page_index: int,
    page_size: int,
    limit: int = None,
):
    model = core.db.get_table_model(tablename, bind)
    return core.db.select(
        model,
        page=page_index,
        per_page=page_size,
        order_by=order_by,
        order_by_direction=direction,
        limit=limit,
    )


def whereused(data_type: str, value, bind: str, column_name: str = None):
    from core import core

    query = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE data_type = 'bigint';
    """
    outputs = {}
    results = core.db.get_query_results(query, bind=bind)
    for r in results:
        if not r["table_name"] in outputs:
            outputs[r["table_name"]] = []
        if column_name is not None:
            matchs = re.findall(column_name, r["column_name"])
            if len(matchs) == 0:
                continue
        outputs[r["table_name"]].append(r["column_name"])
    outputs = {x: list(set(y)) for x, y in outputs.items() if len(y) != 0}

    outputs_f = {}
    for table_name, columns in outputs.items():
        outputs_f[table_name] = {}
        for column in columns:
            query = f"""select * from {table_name} where {column} = {value}"""
            rows = core.db.get_query_results(query, bind=bind)
            if len(rows) != 0:
                outputs_f[table_name][column] = rows
    return outputs_f
