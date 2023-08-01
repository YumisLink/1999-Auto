import lib.find as f
import time
from loguru import logger
import lib.adb_command as adb
import plugins.mission_ready as ready
import plugins.path as path

IMAGE_BASE_EXP = 'imgs/base_exp'
IMAGE_BASE_WILDERNESS = 'imgs/wilderness'
IMAGE_BASE_FRIEND = 'imgs/base_friend'
IMAGE_BASE_MONEY = 'imgs/base_money'
IMGAE_BUILDING_CHECKER = 'imgs/building_checker'
IMAGE_BASE_CHECKER = 'imgs/base_checker'
IMAGE_CHAT_CHECKER = 'imgs/chat_checker'
IMGAE_CHAT = 'imgs/chat'

def back_to_land():
    out=f.cut_find_html(IMGAE_BUILDING_CHECKER,1140,14,1307,81)
    if out[0]is not None:
        logger.debug('误入建筑，返回')
        adb.touch((60,60))
        time.sleep(1)    

def wild_start():
    """领不休荒原产物"""
    while not path.to_menu():
        pass
    adb.touch(f.find(IMAGE_BASE_WILDERNESS))
    logger.info('进入不休荒原')
    while(True):
        time.sleep(3)
        if (f.find(IMAGE_BASE_CHECKER)[2]>0.7):
            break
    adb.touch(f.find(IMAGE_BASE_EXP))
    time.sleep(2)
    back_to_land()#防止进入建筑页面
    adb.touch(f.find(IMAGE_BASE_MONEY))
    time.sleep(2)
    back_to_land()
    xy=f.cut_find_html(IMAGE_BASE_FRIEND,0,112,140,571)
    if xy[0] is not None:
        adb.touch(xy)
    #if (f.find(IMAGE_BASE_FRIEND,False)[2]>0.5):
    #    adb.touch(f.find(IMAGE_BASE_FRIEND,False))
    #处理对话
    time.sleep(2)
    res=f.cut_find_html(IMGAE_CHAT,1462,165,1579,768)
    res2=f.cut_find_html(IMAGE_CHAT_CHECKER,1365,801,1585,890,False)
    if res[0] is not None or res2[0] is not None:
        for _ in range(10):
            if res[0] is not None:
                logger.debug('存在IMAGE_CHAT')
                adb.touch(res)
            if res2[0] is not None:
                logger.debug('存在IMAGE_CHAT_CHECKER')
                adb.touch(res2)
            time.sleep(1)
            res=f.cut_find_html(IMGAE_CHAT,1462,165,1579,768)
            res2=f.cut_find_html(IMAGE_CHAT_CHECKER,1365,801,1585,890,False)
            if res[0] is None and res2[0] is None:
                break
        else:
            return False
    return True