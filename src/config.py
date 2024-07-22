import yaml

NAMES = {
    "key": "ключ",
    ("fields", "issuetype", "self"): "ссылка",
    ("fields", "creator", "self"): "исполнитель",
    ("fields", "customfield_10015"): "дата начала работ",
    ("fields", "issuetype", "name"): "тип задачи",
    ("fields", "created"): "дата создания",
    ("fields", "priority", "name"): "приоритет",
    ("fields", "summary"): "резюме",
}

filename = '../config.yml'
with open(filename, "r") as yaml_file:
    data = yaml.load(yaml_file, Loader=yaml.FullLoader)
CONFIG = data["variables"]
API_KEY = CONFIG["API_KEY"]
HOST = CONFIG["HOST"]
DATABASE = CONFIG["DATABASE"]
TABLE = CONFIG["TABLE"]
CH_HOST = CONFIG["CH_HOST"]
PORT = CONFIG["PORT"]
USER = CONFIG["USER"]
PASSWORD = CONFIG["PASSWORD"]
DB = CONFIG["DB"]