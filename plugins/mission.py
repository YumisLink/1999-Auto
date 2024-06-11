import lib.find as f
import time
import cv2 as cv
import lib.adb_command as adb
import plugins.mission_ready as ready
import plugins.path as path
import lib.ppocr as pp
from lib import api
from plugins import active

from loguru import logger

IMAGE_MISSION = 'imgs/menu_mission'
IMAGE_CLAIM_ALL = 'imgs/mission_claim_all'
IMAGE_CLAIM = 'imgs/mission_claim'
IMAGE_DAY_FIND = 'imgs/mission_day_active'
IMAGE_DAY = 'imgs/mission_day_disable'
IMAGE_WEEK = 'imgs/mission_week'

def mission_start():
    """领取任务奖励"""
    path.to_menu()
    adb.touch(f.find(IMAGE_MISSION,False))
    time.sleep(1.5)

    day = f.find_image(IMAGE_DAY_FIND)
    if '每日' not in pp.ocr_bytes_xy(day,'每日'):
        logger.info("点击每日任务")
        adb.touch(f.find(IMAGE_DAY))
        time.sleep(1)
    
    claim = f.find(IMAGE_CLAIM_ALL)
    logger.debug(f'claim_all匹配: {claim}')
    if (claim[2] > 0.7):
        adb.touch(claim)
        logger.info("完成所有任务")
        time.sleep(4)
        adb.touch(claim)
        time.sleep(1)
    else:
        claim = f.find(IMAGE_CLAIM,False)
        logger.debug(f'claim_single匹配: {claim}')
        if (claim[2] > 0.7):
            adb.touch(claim)
            logger.info("完成单个任务")
            time.sleep(4)
            adb.touch(claim)
            time.sleep(1)

    
    logger.info("点击每周任务")
    adb.touch(f.find(IMAGE_WEEK))
    claim = f.find(IMAGE_CLAIM_ALL)
    logger.debug(f'claim_all匹配: {claim}')
    if (claim[2] > 0.7):
        adb.touch(claim)
        logger.info("完成所有任务")
        time.sleep(2)
        adb.touch(claim)
        time.sleep(1)
    else:
        claim = f.find(IMAGE_CLAIM,False)
        logger.debug(f'claim_single匹配: {claim}')
        if (claim[2] > 0.7):
            adb.touch(claim)
            logger.info("完成单个任务")
            time.sleep(1)
            adb.touch(claim)
            time.sleep(1)


    # adb.touch(f.find(IMAGE_DAY,False))
    
    
def get_fusing_box():
    """获取定影匣子"""
    active.to_festival()
    time.sleep(1)
    screen = api.get_screen_shot()
    ocr_res = pp.ocr_xy(screen, '轶事', cn=True)
    if ocr_res[0] is None:
        logger.error("未找到轶事入口")
        return False
    pos, conf, text = ocr_res
    assert adb.touch((int(pos[0]), int(pos[1]))) == 0
    time.sleep(2)
    
    screen = api.get_screen_shot()
    ocr_res = pp.ocr_xy(screen, '步入故事', cn=True)
    if ocr_res[0] is None:
        logger.error("未找到轶事入口")
        return False
    pos, conf, text = ocr_res
    assert adb.touch((int(pos[0]), int(pos[1]))) == 0
    time.sleep(2)
    return True