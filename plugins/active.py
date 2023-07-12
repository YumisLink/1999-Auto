import plugins.path as path 
import plugins.san as san
import lib.find as f
import time
import lib.adb_command as adb
from config.config import data
import lib.ppocr as pp
import lib.api as api

IMAGE_RESOURCE = "imgs/active_resource"
IMAGE_THE_POUSSIERE = 'imgs/level_poussiere'
"""经验"""
IMAGE_MINTAGE_AESTHETICS = 'imgs/level_mintage_aesthetics'
"""钱"""
IMAGE_HARVEST = 'imgs/level_harvest'
"""基建（丰收时令）"""
IMAGE_ANALYSIS = 'imgs/level_analysis'
"""圣遗物狗粮（意志解析）"""

REPLAY_1 = 1
"""复现1次"""
REPLAY_2 = 2
"""复现2次"""
REPLAY_3 = 3
"""复现3次"""
REPLAY_4 = 4
"""复现4次"""
LEVEL_4 = 4
"""第4关"""
LEVEL_5 = 5
"""第5关"""
LEVEL_6 = 6
"""第6关"""


IMAGE_START = "imgs/START_ACTIVE"
IMAGE_REPLAY = 'imgs/enter_replay_mode2'
IMAGE_REPLAY_SELECT = 'imgs/replay_select'
IMAGE_START_REPLAY = 'imgs/start_replay'
IMGAE_IN_REPLAY='imgs/already_in_replay_mode'
IMAGE_BATTLE_INFO = "imgs/battle_info"
IMAGE_BATTLE_INFO_RESTART = "imgs/battle_info_restart"



def Auto_Active(type: str, level: int, times,go_resource=True,level_swipetimes=10 ):
    """
    进入特定关卡进行复现.
    :param level:第几关.
    :param type:关卡类型.
    :param times:复现次数.
    """    
    if go_resource:
        to_resource()
    exist=f.find((type))
    print('目标关卡识别率：',exist[2])
    if exist[2]>0.7:
        adb.touch(exist)
        time.sleep(1)
    else:
        adb.swipe((1344,485),(156,488))
        time.sleep(1)
        adb.touch(f.find((type)))
        time.sleep(1)
    print(f"正在进入{type}")
    time.sleep(0.8)

    # level_click = f.find(level)
    # print(level_click)
    # if (level_click[2] < 0.6):
    #     adb.swipe((data['y']-100,data['x']/2),(100,data['x']/2))
    #     level_click = f.find(level)
    # adb.touch(level_click)
    to_level(level,level_swipetimes)
    print(f"正在进入{level}")
    time.sleep(0.8) 




    adb.touch(f.find(IMAGE_START))
    print(f"正在进入开始界面菜单")
    time.sleep(4)

    is_replay =f.cut_find_html(IMGAE_IN_REPLAY,883,753,1555,897)
    if is_replay[0] is not None:
        replay = f.find(IMAGE_REPLAY)
        print('replay:',replay)
        if replay[2] > 0.72:
            adb.touch(replay)
            print(f"选择复现模式")
            time.sleep(1.7)
    adb.touch(f.cut_find_html(IMAGE_REPLAY_SELECT,971,782,1100,860))
    print(f"选择复现次数")
    time.sleep(1.7)
    if times>4:
        times=4#最多4次
    adb.touch((1029,768-78*(times-1)))#TODO:分辨率问题，目前写死;1029:按钮的x坐标，768:x1按钮的y坐标，78:每个按钮的高度，times:第几个按钮

    adb.touch(f.find(IMAGE_START_REPLAY))
    print(f"开始复现")
    time.sleep(20)

    while(True):
        adb.touch((50,3))
        time.sleep(4)
        res=f.cut_find_html(IMAGE_START_REPLAY,1128,751,1549,892)
        if res[0] is not None:
            print('复现完成')
            break
        # ans = pp.ocr_bytes_xy(f.find_image(IMAGE_START_REPLAY))
        # if (len(ans)>0):
        #     if ans[2] is not None and '复现' in ans[2]:
        #         break
    # time.sleep(3)
def to_level(level:int,swipetimes=10):
    for i in range(swipetimes+1):
        adb.swipe((1500,744),(200,750))
        time.sleep(0.1)
    for i in range(1,99):
        screen=api.get_scrren_shot_bytes()
        res=f.detect_numbers(screen)
        for num,xy in res:
            if num==level:
                x,y=xy
                y=y+50
                adb.touch([x+70,y+20])#输出坐标为数字左上角坐标，在此修正点击位置
                time.sleep(1)
                return True
        adb.swipe((100,744),(1040,750))
        time.sleep(1)
    return False
        
def to_resource():
    """
    进入资源关.
    """    
    path.to_menu()
    #活动期间先识别反着的提高效率
    res=f.cut_find_html('imgs/enter_the_show2',1162,175,1529,738)
    if res[0] is None:
        x,y=f.cut_find_html('imgs/enter_the_show',1162,175,1529,738)
    else:
        x,y=res
    if not y:
        print('主会场正反都没有，加群联系作者或者提issue吧')
        exit(1)
    adb.touch((x,y+20))
    print("正在进入主会场")
    time.sleep(1)

    adb.touch(f.find(IMAGE_RESOURCE))
    print("点击资源")
    time.sleep(1)
# Auto_Active(IMAGE_MINTAGE_AESTHEICS, LEVEL_6, REPLAY_4)

def active_as_much(type: str, level: int,level_san:int):
    path.to_menu()
    sanum=san.get_san()
    if not sanum:
        print('理智识别失败，退出')
        return None
    print('活力:',sanum)
    intsan=int(sanum)
    total_times=intsan//level_san
    fourtimes=total_times//4
    times=total_times%4
    print('fourtimes:',fourtimes,'times:',times)
    if fourtimes >0:
        for i in range(fourtimes):
            Auto_Active(type, level, 4)
    if times>0:
        Auto_Active(type, level, times)

