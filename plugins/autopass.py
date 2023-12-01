#领取通行证（点唱机）奖励
import time
from loguru import logger
import lib.find as f
import lib.adb_command as adb
import plugins.path as path


IMG_PASS = 'imgs/pass/pass'
IMG_CLAIM_ALL='imgs/pass/claim_all'
IMG_REDPOINT='imgs/pass/redpoint'
IMG_CLAIM='imgs/pass/claim'
IMG_UPGARDE='imgs/pass/upgrade'

def pass_start():
    """领取点唱机奖励"""
    assert path.to_menu()
    adb.touch([270,86])
    # adb.touch((407, 86)) # 箱中巡游版本
    time.sleep(1)

    res = f.cut_find_html('imgs/pass/redpoint',1524,84,1555,50)
    if res[0] is not None:
        logger.info('开始领取')
        #读碟
        adb.touch([1417,98])
        time.sleep(0.3)
    else:
        logger.info('没有奖励可领取')
        return
    #日记
    claim_all()
    claim()
    #周报
    adb.touch([1024,283])
    claim_all()
    claim()
    #公约
    adb.touch([1383,283])
    claim_all()
    claim()

def claim():
    for _ in range(10):
        res=f.cut_find_html(IMG_CLAIM,1410,324,1546,784)
        if res[0] is not None:
            adb.touch(res)
            time.sleep(1.5)
            db_upgarde()
        else:
            return False
    else:
        raise Exception('领取奖励次数异常')
def claim_all():
    res=f.cut_find_html(IMG_CLAIM_ALL,1194,777,1598,897)
    if res[0] is not None:
        adb.touch(res)
        time.sleep(1.5)
        db_upgarde()
        return True
    else:
        return False

def db_upgarde():
    res=f.cut_find_html(IMG_UPGARDE,695,483,881,534)
    if res[0] is not None:
        logger.debug('检测到升级')
        adb.touch([6,899])
        time.sleep(1)
        return True