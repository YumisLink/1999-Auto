import os
import json
import shutil
from typing import cast, Any


def check_path():
    if not os.path.exists('cache'):
        os.mkdir('cache')
    if not os.path.exists('config.json'):
        shutil.copy('config.default.json', 'config.json')
            
check_path()

with open('config.json', 'r') as f:
    global user_config
    user_config = json.load(f)
    user_config = cast(dict[str, Any], user_config)
    
ADB_PATH = user_config["adb_path"]
DEVICE_ID = user_config["device_id"]
ADB_HEAD = user_config["adb_head"]
APPID = "com.shenlan.m.reverse1999" 
ACTIVITY = "com.ssgame.mobile.gamesdk.frame.AppStartUpActivity"
EXEC_USER = ''

def set_channel(channel: str):
    global APPID
    match channel:
        case '官服':
            APPID = "com.shenlan.m.reverse1999"
        case 'B服':
            APPID = "com.shenlan.m.reverse1999.bilibili"
        case _:
            raise KeyError("Invalid channel")

def set_user(user: str):
    global EXEC_USER
    EXEC_USER = user