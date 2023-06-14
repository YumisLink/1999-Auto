import os
import json
from config.config import user_config,ADB_HEAD


def get_screen_shot():
    os.system(f'{ADB_HEAD} exec-out screencap -p > cache/screenshot.png')
    return 'cache/screenshot.png'

def write_config():
    with open('config.json', 'w') as f:
        json.dump(user_config, f, indent=4)
