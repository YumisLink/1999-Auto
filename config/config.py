import os
import json

data = {
    'x': 0,
    'y': 0
}
with open('config.json', 'r') as f:
    global user_config
    user_config = json.load(f)
ADB_PATH = user_config["adb_path"]
DEVICE_ID = user_config["device_id"]
ADB_HEAD = user_config["adb_head"]
APPID = "com.shenlan.m.reverse1999" 

def check_path():
    if not os.path.exists('cache'):
        os.mkdir('cache')
    if not os.path.exists('config.json'):
        config = {
                "adb_path": "",
                "adb_address": "",
                "device_id": "",
                "adb_head": "",
                "bluestacks_conf_path": "",
                "bluestacks_adb_port_keys": ""
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
            
check_path()