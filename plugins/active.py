import plugins.path as path 
import plugins.san as san
import lib.find as f
import time
from loguru import logger
import lib.adb_command as adb
from config.config import data
import lib.ppocr as pp
import lib.api as api

from typing import Callable, Optional

IMAGE_RESOURCE = "imgs/active_resource"
IMAGE_INSIGHT = 'imgs/active/insight'#洞察
IMAGE_THE_POUSSIERE = 'imgs/level_poussiere'#经验
IMAGE_MINTAGE_AESTHETICS = 'imgs/level_mintage_aesthetics'#钱
IMAGE_HARVEST = 'imgs/level_harvest' #基建（丰收时令）
IMAGE_ANALYSIS = 'imgs/level_analysis' #圣遗物狗粮（意志解析）

IMAGE_GREEN_MAINLINE = "imgs/active/green_lake_mainline"

IMAGE_CHAPTER1 = 'imgs/active/chapter1'
IMAGE_CHAPTER2 = 'imgs/active/chapter2'
IMAGE_CHAPTER3 = 'imgs/active/chapter3'
IMAGE_CHAPTER4 = 'imgs/active/chapter4'
IMAGE_CHAPTERX = 'imgs/active/chapter%d'

IMAGE_MOUNTAIN_ECHOS = 'imgs/active/ME'
IMAGE_STARTFALL_LOCALE = 'imgs/active/SL'
IMAGE_SYLVANUS_SHAPE = 'imgs/active/SS'
IMAGE_BRUTES_WILDS = 'imgs/active/BW'
IMAGE_INSIGHT_MAP = {
    '群山之声': IMAGE_MOUNTAIN_ECHOS,
    '星陨之所': IMAGE_STARTFALL_LOCALE,
    '深林之形': IMAGE_SYLVANUS_SHAPE,
    '荒兽之野': IMAGE_BRUTES_WILDS,
}

IMAGE_START = "imgs/START_ACTIVE"
IMAGE_START_HARD = "imgs/active/START_ACTIVE_HARD"
IMAGE_START_GREEN = "imgs/active/START_ACTIVE_GREEN"
IMAGE_REPLAY = 'imgs/enter_replay_mode'
IMAGE_REPLAY_SELECT = 'imgs/replay_select'
IMAGE_START_REPLAY = 'imgs/start_replay'
IMGAE_IN_REPLAY='imgs/already_in_replay_mode'
IMAGE_NOT_IN_REPLAY = 'imgs/active/not_relay_action'
IMAGE_BATTLE_INFO = "imgs/battle_info"
IMAGE_BATTLE_INFO_RESTART = "imgs/battle_info_restart"



def Auto_Active(
    type: str, level: int, times:int,
    go_resource=True,
    level_swipetimes=10,
    choose_hardness: Optional[Callable[[], Optional[str]]]=None,
    as_much=False
):
    """
    进入特定关卡进行复现.
    :param level:第几关.
    :param type:关卡类型.
    :param times:复现次数.
    :param go_resource:是否进入资源关.
    :param level_swipetimes:关卡滑动次数.
    :param choose_hardness:选择难度的函数, 若成功选择, 则返回开始按钮的名称, 否则返回None.
    """    
    if go_resource:
        to_resource()
    exist=f.find(type)
    logger.debug('目标关卡识别率：{}',exist[2])
    if exist[2]>0.7:
        adb.touch(exist)
        time.sleep(1)
    else:
        time.sleep(1)
        adb.swipe((1344,485),(156,488))
        time.sleep(1)
        adb.touch(f.find((type)))
        time.sleep(1)
    logger.info(f"进入{type}")
    time.sleep(0.8)

    assert to_level(level, level_swipetimes)
    time.sleep(0.8) 

    if choose_hardness:
        start_btn = choose_hardness()
    else:
        start_btn = IMAGE_START
    
    if start_btn is None:
        raise Exception('选择难度失败')
    if as_much:
        level_san=san.get_levelsan()
        player_san=san.detect_san_in_level()
        total_times=player_san//level_san
        fourtimes=total_times//4
        times=total_times%4
        logger.info(f"打: {fourtimes}次4倍，1次{times}倍复现")
        adb.touch(f.find(start_btn))
        logger.info(f"进入行动界面")
        time.sleep(4)
        if fourtimes >0:
            for i in range(fourtimes):
                sub_replay(4)
        if times>0:
            sub_replay(times)
    else:
        adb.touch(f.find(start_btn))
        logger.info(f"进入行动界面")
        time.sleep(4)

        sub_replay(times)
        
def to_level(level:int,swipetimes=2):
    logger.info(f'开始寻找第{level}关')
    for _ in range(swipetimes+1):
        adb.swipe((1500,744),(300,750))
        time.sleep(1)
    for i in range(20):
        screen=api.get_scrren_shot_bytes()
        res=f.detect_numbers(screen)
        for num,xy in res:
            if num==level:
                x,y=xy
                y=y+50
                adb.touch([x+70,y+20])#输出坐标为数字左上角坐标，在此修正点击位置
                time.sleep(1)
                logger.info(f"进入第{level}关")
                return True
        logger.debug(f'第{i}次识别，未找到目标关卡，继续滑动')
        adb.swipe((500,744),(1040,750), 300)
        time.sleep(1)
    return False

def sub_replay(times:int):
    is_replay =f.cut_match_html(IMGAE_IN_REPLAY,883,753,1555,897)
    is_replay2=f.cut_match_html(IMAGE_NOT_IN_REPLAY,981,706,1556,882)
    if is_replay is None or is_replay[2] < 0.7 or is_replay2 is not None or is_replay2[2] > 0.7:
        logger.debug('不在复现模式')
        replay = f.cut_find_html(IMAGE_REPLAY,819,736,1126,895)
        if replay[0] is not None:
            adb.touch(replay)
            logger.debug(f"选择复现模式")
            time.sleep(1.7)   

    adb.touch(f.cut_find_html(IMAGE_REPLAY_SELECT,971,782,1100,860))
    logger.debug(f"选择复现次数")
    time.sleep(1.7)
    if times>4:
        times=4#最多4次
    adb.touch((1029,768-78*(times-1)))#TODO:分辨率问题，目前写死;1029:按钮的x坐标，768:x1按钮的y坐标，78:每个按钮的高度，times:第几个按钮
    
    time.sleep(1)
    adb.touch(f.find(IMAGE_START_REPLAY))
    logger.info(f"开始复现")
    time.sleep(60)

    while(True):
        adb.touch((6,887)) 
        time.sleep(4)
        res=f.cut_find_html(IMAGE_START_REPLAY,1128,751,1549,892)
        if res[0] is not None:
            logger.info('复现完成')
            break

def enter_the_show():
    path.to_menu()
    #活动期间先识别反着的提高效率
    res=f.cut_find_html('imgs/enter_the_show2',1162,175,1529,738)
    if res[0] is None:
        x,y=f.cut_find_html('imgs/enter_the_show',1162,175,1529,738)
    else:
        x,y=res
    if not y:
        logger.error('主会场正反都没有，加群联系作者或者提issue吧')
        raise Exception('进入主会场失败')
    adb.touch((x,y+20))
    logger.info("正在进入主会场")
    time.sleep(1)

def to_resource():
    """
    进入资源关.
    """    
    enter_the_show()
    adb.touch(f.find(IMAGE_RESOURCE))
    logger.info("点击资源")
    time.sleep(1)

def to_insight():
    """
    进入洞悉关.
    """    
    enter_the_show()
    adb.touch(f.find(IMAGE_INSIGHT))
    logger.info("点击洞悉")
    time.sleep(1)

def to_festival():
    """
    进入活动关（即点击主会场的上面一些的位置，此方法以后可能会失效）
    """
    path.to_menu()
    #活动期间先识别反着的提高效率
    res=f.cut_find_html('imgs/enter_the_show2',1162,175,1529,738)
    if res[0] is None:
        x,y=f.cut_find_html('imgs/enter_the_show',1162,175,1529,738)
    else:
        x,y=res
    if not x or not y:
        logger.error('识别主会场失败')
        raise Exception('识别主会场失败')
    adb.touch((x+20, y-40))
    logger.info("进入活动")
    time.sleep(1)

def to_story(chapter:int):
    """
    进主线.
    :param chapter:第几章.
    :param level:第几关.
    :param times:复现次数.
    :param is_hard:是否为厄险模式.
    因为主线有厄险所以单列
    """    
    enter_the_show()

    adb.touch([178,817])
    logger.info("点击故事")
    time.sleep(1)

    adb.touch(f.find('imgs/active/chapter'+str(chapter)))
    logger.info("点击第"+str(chapter)+"章")
    time.sleep(1)



def choose_story_disaster():
    res = pp.cut_html_ocr_bytes_xy(api.get_scrren_shot_bytes(), 1112,291,1525,365, '厄险')
    if res[0] is not None:
        adb.touch(res[0])
        logger.debug('点击厄险')
        time.sleep(1)
        return IMAGE_START_HARD
    else:
        logger.error('未找到厄险，退出')
        return None

def detect_hard_green():
    ocr_res = pp.cut_html_ocr_bytes(api.get_scrren_shot_bytes(), 1270, 300, 1350, 340)
    assert ocr_res['code'] == 100
    res: list[dict] = ocr_res['data']
    res = sorted(res, key=lambda x: -x['score'])[0]
    return ['故事', '意外', '艰难'].index(res['text']) + 1

def choose_green_lake(hard: int):
    now_hard = detect_hard_green()
    logger.info(f'当前难度：{now_hard}, 目标难度：{hard}')
    while now_hard < hard:
        adb.touch((1490, 315))
        time.sleep(1)
        now_hard += 1
    while now_hard > hard:
        adb.touch((1130, 315))
        time.sleep(1)
        now_hard -= 1
    now_hard = detect_hard_green()
    assert now_hard == hard
    return IMAGE_START_GREEN

def active_as_much(type: str, level: int,level_san:int):
    path.to_menu()
    sanum=san.get_san()
    if not sanum:
        logger.warning('理智识别失败，退出')
        return None
    logger.info('活力:',sanum)
    intsan=int(sanum)
    total_times=intsan//level_san
    fourtimes=total_times//4
    times=total_times%4
    logger.info(f"打:{fourtimes}次4倍，{times}次1倍复现")
    if fourtimes >0:
        for i in range(fourtimes):
            Auto_Active(type, level, 4)
    if times>0:
        Auto_Active(type, level, times)

