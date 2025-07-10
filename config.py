import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CONFIG_PATH_RU = "/usr/local/etc/xray/ru_config.json"
CONFIG_PATH_US = "/usr/local/etc/xray/us_config.json"

DOMAIN_RU = "ru.independentvpn.ru"
DOMAIN_US = "us.independentvpn.ru"

XRAY_RESTART_CMD = "systemctl restart xray"

SSH_SERVERS = {
    "ru": {
        "host": "194.87.74.91",
        "port": 443,
        "username": "root",
        "password": "KfpZ81gwpx",  # или используем ключи
        "config_path": "/usr/local/etc/xray/config.json",
        "domain": "ru.independentvpn.ru"
    },
    "us": {
        "host": "185.106.95.235",
        "port": 443,
        "username": "root",
        "password": "j~W6eXDvBAGIfGFig",
        "config_path": "/usr/local/etc/xray/config.json",
        "domain": "us.independentvpn.ru"
    }
}
