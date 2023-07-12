import cv2 as cv
from time import sleep

import plugins.path as path
import lib.find as f
import lib.ppocr as pp
import lib.adb_command as adb
import lib.api as api


def get_san():
    status=path.where_am_i()
    if status == 'menu':
        adb.touch([1460,204])
        sleep(1)
        out=detect_san_in_san()
        return out
    elif status == 'san':
        out=detect_san_in_san()
        return out

    elif status == 'notmenu2' or status == 'notmenu' or status == 'nothome':
        is_san=f.cut_find_html('imgs/san_checker',1325,8,1448,72)
        if is_san[0]is not None:
            api.get_screen_shot()
            out=pp.cut_html_ocr_bytes(cv.imread('cache/screenshot.png'),1338,2,1598,75)
            if out['code'] != 100:
                print(out)
                return None
            text=out['data']['text']
            return (text)
    else:
        print('未找到活力值')
        return None
    
def detect_san_in_san():
    api.get_screen_shot()
    out=pp.cut_html_ocr_bytes(cv.imread('cache/screenshot.png'),675,674,853,764)
    if out['code'] != 100:
        print(out)
        return None
    text=out['data'][0]['text']
    return int(text)
