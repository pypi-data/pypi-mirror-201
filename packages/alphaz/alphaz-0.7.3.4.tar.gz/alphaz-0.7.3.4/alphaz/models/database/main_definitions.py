import json
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint,
    Float,
    BLOB,
)

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref

from ...libs.string_lib import create_hash

from .models import (
    AlphaTable,
    AlphaTableId,
    AlphaColumn,
    AlphaFloat,
    AlphaInteger,
    AlphaTableIdUpdateDate,
    AlphaTableUpdateDate,
)
from .tests import Test, TestChild, TestChilds
import datetime, inspect, ast

from core import core, DB

ma = core.ma


class FilesProcess(DB.Model, AlphaTableUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "files_process"
    ensure = True

    name = AlphaColumn(String(40), nullable=False, primary_key=True)
    key = AlphaColumn(String(100), nullable=False, primary_key=True)
    filename = AlphaColumn(String(100), nullable=False, primary_key=True)
    modifiation_time = AlphaColumn(Integer)
    filesize = AlphaColumn(Integer)
    lifetime = AlphaColumn(Integer)
    error = AlphaColumn(Integer)


class Processes(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "processes"

    uuid = AlphaColumn(String(36))
    name = AlphaColumn(String(20), primary_key=True)
    parameters = AlphaColumn(String(20), primary_key=True)
    status = AlphaColumn(String(5))

    __table_args__ = (
        UniqueConstraint("name", "parameters", name="processes_constraint"),
    )


class Logs(DB.Model, AlphaTableId):
    __bind_key__ = "MAIN"
    __tablename__ = "logs"

    update_date = AlphaColumn(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        primary_key=True,
    )
    level = AlphaColumn(String(10), primary_key=True)
    type_ = AlphaColumn(String(30), primary_key=True)
    origin = AlphaColumn(String(30), primary_key=True)
    message = AlphaColumn(Text)
    stack = AlphaColumn(Text)


class Tests(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "tests"

    category = AlphaColumn(String(50), primary_key=True)
    tests_group = AlphaColumn(String(50), primary_key=True)
    name = AlphaColumn(String(50), primary_key=True)

    status = AlphaColumn(Integer)
    start_time = AlphaColumn(DateTime)
    end_time = AlphaColumn(DateTime)
    elapsed = AlphaColumn(Float)


class Request(DB.Model, AlphaTable):
    __bind_key__ = "MAIN"
    __tablename__ = "request"

    index = AlphaColumn(Integer, primary_key=True, autoincrement=True)
    response_time = AlphaColumn(Float)
    date = AlphaColumn(DateTime)
    method = AlphaColumn(String(6))
    size = AlphaColumn(Integer)
    status_code = AlphaColumn(Integer)
    path = AlphaColumn(String(100))
    user_agent = AlphaColumn(String(200))
    remote_address = AlphaColumn(String(20))
    exception = AlphaColumn(String(500))
    referrer = AlphaColumn(String(100))
    browser = AlphaColumn(String(100))
    platform = AlphaColumn(String(20))
    mimetype = AlphaColumn(String(30))


class NewsLetter(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "newsletter"
    name = AlphaColumn(String(100), primary_key=True)
    mail = AlphaColumn(String(50), primary_key=True)


class ProcesseLog(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "process_log"

    uuid = AlphaColumn(String(36))
    name = AlphaColumn(String(20), primary_key=True)
    parameters = AlphaColumn(String(100), primary_key=True)
    status = AlphaColumn(String(5))


def _parameters_to_string(parameters):
    return ";".join([str(x) for x in parameters.values()])
class MailHistory(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "mail_history"

    uuid = AlphaColumn(String(50), primary_key=True)
    mail_type = AlphaColumn(String(250))
    parameters = AlphaColumn(String(200))
    parameters_full = AlphaColumn(String(500))
    date = AlphaColumn(DateTime)

    hash_key = AlphaColumn(String(64), unique=True, nullable=False)

    def __init__(self, uuid, mail_type, parameters, parameters_full, *args):
        super().__init__(*args)
        self.uuid = uuid
        self.mail_type = mail_type
        self.parameters = json.dumps(parameters)
        self.parameters_full = json.dumps(parameters_full)
        self.hash_key = create_hash(mail_type, _parameters_to_string(parameters), _parameters_to_string(parameters_full))

class MailBlacklist(DB.Model, AlphaTableId):
    __bind_key__ = "MAIN"
    __tablename__ = "mail_blacklist"
    __table_args__ = (
        UniqueConstraint("mail", "mail_type", name="unique_component_commit"),
    )

    mail = AlphaColumn(String(50), primary_key=True)
    mail_type = AlphaColumn(String(20), primary_key=True)


class Constants(DB.Model, AlphaTableUpdateDate):
    __tablename__ = "constants"
    __bind_key__ = "MAIN"

    name = AlphaColumn(String(30), primary_key=True)
    type = AlphaColumn(String(10))
    value = AlphaColumn(String(100))


class Parameters(DB.Model, AlphaTableUpdateDate):
    __tablename__ = "parameters"
    __bind_key__ = "MAIN"

    name = AlphaColumn(String(30), primary_key=True)
    value = AlphaColumn(Text)


class Configs(DB.Model, AlphaTableUpdateDate):
    __tablename__ = "configs"
    __bind_key__ = "MAIN"

    name = AlphaColumn(String(30), primary_key=True)
    type = AlphaColumn(String(10))
    value = AlphaColumn(Text)

