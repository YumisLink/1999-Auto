import mission_ready
import find as f
import time
import adb_command as adb
from config.config import data

IMAGE_RESOURCE = "imgs/active_resource"
IMAGE_THE_POUSSIERE = 'imgs/THE_POUSSIERE'
IMAGE_MINTAGE_AESTHEICS = 'imgs/MINTAGE_AESTHEICS'

REPLAY_1 = (0.63, 0.85)
REPLAY_2 = (0.63, 0.76)
REPLAY_3 = (0.63, 0.68)
REPLAY_4 = (0.63, 0.59)
LEVEL_4 = 'imgs/4'
LEVEL_5 = 'imgs/5'
LEVEL_6 = 'imgs/6'


IMAGE_START = "imgs/START_ACTIVE"
IMAGE_REPLAY = 'imgs/enter_replay_mode2'
IMAGE_REPLAY_SELECT = 'imgs/replay_select'
IMAGE_START_REPLAY = 'imgs/start_replay'
# IMAGE_HARVEST_PRIME =
# IMAGE_ANALYSIS =


def Auto_Active(level: str, type: str, times: str):
    if not mission_ready.ready():
        raise RuntimeError('无法返回主菜单')
    adb.touch(f.find('imgs/enter_the_show'))
    print("正在进入主会场")
    time.sleep(0.4)
    adb.touch(f.find(IMAGE_RESOURCE))
    print("正在资源")
    time.sleep(0.4)
    adb.touch(f.find(level))
    print(f"正在进入{level}")
    time.sleep(0.5)
    adb.touch(f.find(type))
    print(f"正在进入{type}")
    time.sleep(0.5)
    adb.touch(f.find(IMAGE_START))
    print(f"正在进入开始界面菜单")
    time.sleep(2.5)
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
        time.sleep(3)
        ans = f.find('imgs/VICTOR')
        if ans[2] > 0.67:
            adb.touch(ans)
            break
    time.sleep(3)


# Auto_Active(IMAGE_MINTAGE_AESTHEICS, LEVEL_6, REPLAY_4)
