import os
import json
import cv2 as cv
import config.config as config

from loguru import logger

def get_screen_shot():
    os.system(f'{config.ADB_HEAD} exec-out screencap -p > cache/screenshot.png')
    return 'cache/screenshot.png'

def get_scrren_shot_bytes():
    os.system(f'{config.ADB_HEAD} exec-out screencap -p > cache/screenshot.png')
    img=cv.imread('cache/screenshot.png')
    return img

def write_config():
    adb_path = config.user_config["adb_path"]
    if 'device_id' in config.user_config and config.user_config['device_id'].strip():
        config.ADB_HEAD = f'{adb_path} -s {config.user_config["device_id"]}'
    else:
        config.ADB_HEAD = f'{adb_path}'
    logger.debug('已重组config.ADB_HEAD:',config.ADB_HEAD)  
    config.user_config['adb_head'] = config.ADB_HEAD #TODO:adb head的使用逻辑有问题，更新之后没法第一时间利用，就非得重启几次程序才能用
    with open('config.json', 'w') as f:
        json.dump(config.user_config, f, indent=4)
