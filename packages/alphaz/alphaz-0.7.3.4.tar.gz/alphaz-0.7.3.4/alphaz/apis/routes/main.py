import datetime, os, inspect, re, platform
from typing import List

from flask import request, send_from_directory

from ...libs import test_lib, database_lib, api_lib, py_lib, files_lib, config_lib
from ...utils.api import route, Parameter
from ...models.main import AlphaException

from core import core, DB, API

LOG = core.get_logger("api")


@API.route("/assets/<path:path>")
def send_js(path):
    return send_from_directory("assets", path)


@API.route("/images/<path:path>")
def send_images(path):
    return send_from_directory("images", path)


@route("/page", parameters=[Parameter("page", required=True, ptype=str)])
def index():
    API.set_html(API.get("page"))


@route("/profil/pic", logged=True)
def get_profil_pic():
    file_path = core.config.get("directories/images")
    API.get_file(file_path, API.get_logged_user().id)


@route("/files/upload", logged=True, methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    ext = uploaded_file.filename.split(".")[1]
    filename = str(API.get_logged_user().id) + "." + ext

    file_path = core.config.get("directories/images")
    API.set_file(file_path, filename)


@route("status", route_log=False)
def status():
    return True


@route("/", route_log=False)
def home():
    config = API.conf

    tests = None
    try:
        tests = test_lib.get_tests_auto()
    except Exception as ex:
        LOG.error(ex)

    mode_color = (
        "#e74c3c"
        if core.config.configuration == "prod"
        else ("#0270D7" if core.config.configuration == "dev" else "#2ecc71")
    )

    parameters = {
        "mode": core.config.configuration,
        "mode_color": mode_color,
        "title": config.get("templates/home/title"),
        "description": config.get("templates/home/description"),
        "year": datetime.datetime.now().year,
        "users": 0,
        "ip": request.environ["REMOTE_ADDR"],
        "admin": config.get("admin_databases"),
        "routes": api_lib.get_routes_infos(log=LOG),
        "compagny": config.get("parameters/compagny"),
        "compagny_website": config.get("parameters/compagny_website"),
        "dashboard": config.get("dashboard/dashboard/active"),
        "tests": tests,
        "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "conda_env": os.environ.get("CONDA_DEFAULT_ENV"),
        "alphaz_version": "",
    }
    API.set_html("home.html", parameters=parameters)


@route("doc", mode="html")
def doc():
    try:
        import markdown2
    except:
        raise AlphaException("import_error", {"module": "markdown"})

    with open("alphaz/help.md", "r") as f:
        content = f.read()
        html = markdown2.markdown(content)
        return html


@route("loggers")
def get_loggers():
    return core.config.loggers


@route(
    "logger/level",
    parameters=[
        Parameter("name", required=True),
        Parameter("level", options=["info", "warnings", "error", "debug"]),
    ],
)
def set_logger_level():
    logger = core.get_logger(API["name"])
    if logger is None:
        raise AlphaException("no_logger")
    logger.set_level(API["level"])


@route("infos")
def get_infos():
    import getpass, platform, sys

    return {
        "user": getpass.getuser(),
        "system": {
            "os": platform.uname().system,
            "node": platform.uname().node,
            "release": platform.uname().release,
            "version": platform.uname().version,
            "machine": platform.uname().machine,
            "processor": platform.uname()[4],
        },
        "version": core.config.get("version"),
        "python": sys.version_info,
    }


@route("/memory")
def get_memory_usage():
    from guppy3 import hpy

    h = hpy()
    return h.heap()


@route("/module", parameters=[Parameter("name", required=True), Parameter("function")])
def get_module_code():
    import importlib

    module = importlib.import_module(API["name"])
    if API["function"] is not None:
        lines = inspect.getsource(getattr(module, API["function"]))
        return {
            "version": str(module.__version__),
            "code": str(lines),
        }
    return {"version": module.__version__}


@route("modules", parameters=[Parameter("name"), Parameter("url"), Parameter("mode")])
def get_modules():
    return py_lib.get_modules_infos(**API.gets())


@route("cache")
def get_cache_infos():
    return files_lib.get_size(API.conf.get("directories/cache"), with_unit=True)


@route(
    "configurations",
    parameters=[Parameter("config_path"), Parameter("name"), Parameter("path")],
    admin=True,
)
def get_configurations():
    from ...models.config import _config

    path_filter = API.get("config_path", None)
    output = {}
    for path, configuration in _config._CONFIGURATIONS.items():
        if (path_filter is not None) and (len(re.findall(path_filter, path)) == 0):
            continue
        if (API.get("name", None)) is not None and API.get(
            "name"
        ) != configuration.name:
            continue
        if (API.get("path", None)) is not None:
            output[path] = {
                "name": configuration.name,
                "data": configuration.get(API.get("path")),
            }
        else:
            output[path] = {
                "name": configuration.name,
                "data": configuration.data,
            }
    return output


@route("dataclasses/mappings")
def get_dataclasses_mappings():
    from ...models.main._base import DATACLASS_AUTO_MAP_MATCHS

    # TODO: update: no need to speciy to_json
    return {x: y.to_json() for x, y in DATACLASS_AUTO_MAP_MATCHS.items()}


@route("/configs", admin=True)
def get_configs():
    return config_lib.get_configs()


@route(
    "/configs/get",
    parameters=[
        Parameter("keys", ptype=list, required=True),
        Parameter("config"),
    ],
)
def get_configs_key():
    return config_lib.get_configs_key(**API.get_parameters())

@route('/mail', parameters=[
    Parameter("name", required=True),
    Parameter("parameters", ptype=List[dict])
],admin=True, methods=["POST"])
def mail_me():
    from ...libs import mail_lib
    mail_lib.send_mail(
        mail_config=API["name"], parameters_list=API["parameters"], force=True
    )