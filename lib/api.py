import os
import json

with open('config.json', 'r') as f:
    config = json.load(f)
adb_head = config['adb_head']
appid = 'com.shenlan.m.reverse1999' 

def get_screen_shot():
    os.system(f'{adb_head} exec-out screencap -p > cache/screenshot.png')
    return 'cache/screenshot.png'

def write_config():
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
