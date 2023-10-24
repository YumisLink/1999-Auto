import os
import json
import cv2 as cv
import config.config as config


def get_screen_shot():
    os.system(f'{config.ADB_HEAD} exec-out screencap -p > cache/screenshot.png')
    return 'cache/screenshot.png'

def get_scrren_shot_bytes():
    os.system(f'{config.ADB_HEAD} exec-out screencap -p > cache/screenshot.png')
    img=cv.imread('cache/screenshot.png')
    return img

def write_config():
    with open('config.json', 'w') as f:
        json.dump(config.user_config, f, indent=4)
