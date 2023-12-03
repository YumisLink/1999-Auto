import cv2 as cv
from time import sleep
from loguru import logger
import plugins.path as path
import lib.find as f
import lib.ppocr as pp
import lib.adb_command as adb
import lib.api as api


def get_san() -> int|None:
    status=path.where_am_i()
    logger.debug('当前界面:',status)
    if status == 'menu':
        # adb.touch([1460,204])
        adb.touch((1525, 200)) # 箱中巡游版本
        sleep(2)
        out=detect_san_in_san()
        adb.touch([1460,204]) # 返回
        return out
    elif status == 'san':
        #在活力值界面识别
        out=detect_san_in_san()
        return out

    elif status == 'notmenu2' or status == 'notmenu' or status == 'nothome':
        #在关卡界面识别(右上角有活力值时)
        return detect_san_in_level()
    else:
        logger.warning('未找到活力值')
        return None
    
def detect_san_in_san():
    api.get_screen_shot()
    out=pp.cut_html_ocr_bytes(cv.imread('cache/screenshot.png'),682,675,859,767)
    if out['code'] != 100:
        logger.debug(out)
        return None
    text=out['data'][0]['text']
    return int(text)

def detect_san_in_level():
    is_san=f.cut_find_html('imgs/san_checker',1325,8,1448,72)
    if is_san[0]is not None:
        api.get_screen_shot()
        out=pp.cut_html_ocr_bytes(cv.imread('cache/screenshot.png'),1429,29,1500,63)
        if out['code'] != 100:
            logger.debug(out)
            return None
        text=out['data'][0]['text']
        return int(text)
    else:
        logger.warning('未找到活力值')
        return None
    
def get_levelsan():
    #只在进入关卡前界面可用
    out=pp.cut_html_ocr_bytes(api.get_scrren_shot_bytes(),1094,651,1371,888)
    if out['code'] != 100:
        logger.debug(out)
        return None
    for item in out['data']:
        if item['score'] > 0.65 and item['text'].strip('-').isdigit():
            return int(item['text'].strip('-'))
    logger.warning(f'没有找到数字{out}')
    return None

def get_maxsan() -> int|None:
    status=path.where_am_i()
    logger.debug('当前界面:',status)
    if status == 'menu':
        adb.touch([1460,204])
        sleep(2)
        out=detect_maxsan()
        adb.touch([1460,204]) # 返回
        return out
    elif status == 'san':
        return detect_maxsan()
    else:
        logger.warning('未找到活力值')
        return None
    
def detect_maxsan() -> int|None:
    out=pp.cut_html_ocr_bytes(api.get_scrren_shot_bytes(),866,721,930,773)
    if out['code'] != 100:
        logger.debug(out)
        return None
    text=out['data'][0]['text']
    return int(text)



#自动吃24小时内的糖
def eat_24H_sugar():
    status=path.where_am_i()
    logger.debug('当前界面:',status)
    if status == 'san':
        out=pp.cut_html_ocr_bytes_xy(api.get_scrren_shot_bytes(),1040,253,1228,392, '小时')
        if out[0] is not None:
            adb.touch((out[0][0],out[0][1]-120))#时间上面才是糖
            logger.debug('点击糖')
            if f.wait_until_find("imgs/confirm",20,True) is None:
                return False
            adb.touch(f.cut_find_html('imgs/confirm',612,458,1596,724))
            logger.debug('点击确认')
            return True
        else:
            logger.error('未找到"小时",退出')
            return False