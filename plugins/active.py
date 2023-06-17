import plugins.mission_ready as mission_ready
import lib.find as f
import time
import lib.adb_command as adb
from config.config import data
import lib.ppocr as pp

IMAGE_RESOURCE = "imgs/active_resource"
IMAGE_THE_POUSSIERE = 'imgs/level_poussiere'
"""经验"""
IMAGE_MINTAGE_AESTHETICS = 'imgs/level_mintage_aesthetics'
"""钱"""
IMAGE_HARVEST = 'imgs/level_harvest'
"""基建"""
IMAGE_ANALYSIS = 'imgs/level_analysis'
"""圣遗物狗粮"""

REPLAY_1 = (0.63, 0.85)
"""复现1次"""
REPLAY_2 = (0.63, 0.76)
"""复现2次"""
REPLAY_3 = (0.63, 0.68)
"""复现3次"""
REPLAY_4 = (0.63, 0.59)
"""复现4次"""
LEVEL_4 = 'imgs/4'
"""第4关"""
LEVEL_5 = 'imgs/5'
"""第5关"""
LEVEL_6 = 'imgs/6'
"""第6关"""


IMAGE_START = "imgs/START_ACTIVE"
IMAGE_REPLAY = 'imgs/enter_replay_mode2'
IMAGE_REPLAY_SELECT = 'imgs/replay_select'
IMAGE_START_REPLAY = 'imgs/start_replay'


def Auto_Active(level: str, type: str, times: str):
    """
    从id中匹配图片并返回其在截图中的样子
    :param level:第几关.
    :param type:关卡类型.
    :param times:复现次数.
    """    
    if not mission_ready.ready():
        raise RuntimeError('无法返回主菜单')
    adb.touch(f.find('imgs/enter_the_show'))
    print("正在进入主会场")
    time.sleep(1)


    adb.touch(f.find(IMAGE_RESOURCE))
    print("点击资源")
    time.sleep(1)

    level_click = f.find(level)
    print(level_click)
    if (level_click[2] < 0.6):
        adb.swipe((data['y']-100,data['x']/2),(100,data['x']/2))
        level_click = f.find(level)
    adb.touch(level_click)
    print(f"正在进入{level}")
    time.sleep(0.8)

    adb.touch(f.find(type))
    print(f"正在进入{type}")
    time.sleep(0.8)



    adb.touch(f.find(IMAGE_START))
    print(f"正在进入开始界面菜单")
    time.sleep(3.5)


    replay = f.find(IMAGE_REPLAY)
    print(replay)
    if replay[2] > 0.72:
        adb.touch(replay)
        print(f"选择复现模式")
    time.sleep(1.7)
    adb.touch(f.find(IMAGE_REPLAY_SELECT))
    print(f"选择复现程度")
    adb.touch((data['y'] * times[0], data['x'] * times[1]))

    adb.touch(f.find(IMAGE_START_REPLAY))
    print(f"开始复现")
    time.sleep(20)

    while(True):
        adb.touch((50,data['x']/2))
        time.sleep(3)
        ans = pp.ocr_bytes_xy(f.find_image(IMAGE_START_REPLAY))
        if (len(ans)>0):
            if ans[2] is not None and '复现' in ans[2]:
                break
    # time.sleep(3)


# Auto_Active(IMAGE_MINTAGE_AESTHEICS, LEVEL_6, REPLAY_4)
