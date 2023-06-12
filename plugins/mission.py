import lib.find as f
import time
import cv2 as cv
import lib.adb_command as adb
import plugins.mission_ready as ready
import cnocr


IMAGE_MISSION = 'imgs/menu_mission'
IMAGE_CLAIM_ALL = 'imgs/mission_claim_all'
IMAGE_CLAIM = 'imgs/mission_claim'
IMAGE_DAY_FIND = 'imgs/mission_day_active'
IMAGE_DAY = 'imgs/mission_day_disable'
IMAGE_WEEK = 'imgs/mission_week'

def mission_start():
    if not ready.ready():   
        raise RuntimeError('无法返回主页面')
    adb.touch(f.find(IMAGE_MISSION,False))
    time.sleep(1)


    time.sleep(1.5)
    day = f.find_image(IMAGE_DAY_FIND)
    ocr = cnocr.CnOcr()
    if '每日' not in ocr.ocr(day)[0]['text']:
        adb.touch(f.find(IMAGE_DAY))
        print("点击每日任务")
        time.sleep(0.5)
    
    claim = f.find(IMAGE_CLAIM_ALL)
    if (claim[2] > 0.7):
        adb.touch(claim)
        print("完成所有任务")
        time.sleep(8)
        adb.touch(claim)
    else:
        claim = f.find(IMAGE_CLAIM,False)
        if (claim[2] > 0.7):
            adb.touch(claim)
            print("完成单个任务")
            time.sleep(8)
            adb.touch(claim)

    
    adb.touch(f.find(IMAGE_WEEK))
    print("点击每周任务")
    claim = f.find(IMAGE_CLAIM_ALL)
    print(claim)
    if (claim[2] > 0.7):
        adb.touch(claim)
        print("完成所有任务")
        time.sleep(2)
        adb.touch(claim)
    else:
        claim = f.find(IMAGE_CLAIM,False)
        if (claim[2] > 0.7):
            adb.touch(claim)
            print("完成单个任务")
            time.sleep(1)
            adb.touch(claim)


    # adb.touch(f.find(IMAGE_DAY,False))
    
    