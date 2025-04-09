import requests
from enum import Enum

from loguru import logger

END_POINT = "http://10.1.0.1:4000"
hostname = "1999-AUTO"

class LogLevel(Enum):
    debug = 0
    info = 1
    warn = 2
    error = 3
    fatal = 4

def log_to_vortana(level: LogLevel, message: str, data: dict = None):
    item = {
        "host": hostname,
        "level": level.name,
    }
    item["message"] = message
    if data is not None:
        item["data"] = data
    
    try:
        res = requests.post(END_POINT, json=item, timeout=1)
    except requests.exceptions.Timeout:
        logger.warning("Timeout when sending log to Vortana.")
        return

    res.raise_for_status()

if __name__ == "__main__":
    log_to_vortana(LogLevel.error, f"Error occurred.")
    log_to_vortana(LogLevel.info, f"Info message.")