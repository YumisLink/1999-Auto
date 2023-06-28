import os
import json
import cv2 as cv
from config.config import user_config,ADB_HEAD


def get_screen_shot():
    os.system(f'{ADB_HEAD} exec-out screencap -p > cache/screenshot.png')
    return 'cache/screenshot.png'

def get_scrren_shot_bytes():
    os.system(f'{ADB_HEAD} exec-out screencap -p > cache/screenshot.png')
    img=cv.imread('cache/screenshot.png')
    return img

def write_config():
    with open('config.json', 'w') as f:
        json.dump(user_config, f, indent=4)
