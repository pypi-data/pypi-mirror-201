# MODULES
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm.attributes import InstrumentedAttribute

# UTILS
from ..utils import *

# CORE
from core import core

DB = core.db


class AlphaModelView(ModelView):
    column_display_pk = True


def load_views(log) -> List[ModelView]:
    """[Load view from tables definitions module]

    Args:
        module (ModuleType): [description]

    Returns:
        List[ModelView]: [description]
    """
    views = []

    for model in DB.get_tables_models():
        table_name = model.__tablename__
        bind = model.__bind_key__

        attributes = [
            x for x, y in model.__dict__.items() if isinstance(y, InstrumentedAttribute)
        ]

        name = "%s:%s" % (bind, table_name)
        view = AlphaModelView(
            table_name,
            DB.session,
            name=table_name,
            category=bind,
            endpoint=name,
        )

        view.column_list = attributes
        views.append(view)
    if len(views) != 0:
        log.info(f"Loaded {len(views)} views models")
    return views
