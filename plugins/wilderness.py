import lib.find as f
import time
import lib.adb_command as adb
import plugins.mission_ready as ready

IMAGE_BASE_EXP = 'imgs/base_exp'
IMAGE_BASE_WILDERNESS = 'imgs/wilderness'
IMAGE_BASE_FRIEND = 'imgs/base_friend'
IMAGE_BASE_MONEY = 'imgs/base_money'
IMGAE_BUILDING_CHECKER = 'imgs/building_checker'
IMAGE_BASE_CHECKER = 'imgs/base_checker'

def to_land():
    out=f.cut_find_html(IMGAE_BUILDING_CHECKER,1124,14,1307,81)
    if out is not None:
        adb.touch((60,60))
        time.sleep(1)    

def wild_start():
    """领不休荒原产物"""
    if not ready.ready():   
        raise RuntimeError('无法返回主页面')
    adb.touch(f.find(IMAGE_BASE_WILDERNESS))
    while(True):
        time.sleep(2)
        if (f.find(IMAGE_BASE_CHECKER)[2]>0.7):
            break
    adb.touch(f.find(IMAGE_BASE_EXP))
    time.sleep(0.1)
    to_land()#防止进入建筑页面
    adb.touch(f.find(IMAGE_BASE_MONEY))
    time.sleep(0.5)
    to_land()
    xy=f.cut_find_html(IMAGE_BASE_FRIEND,0,112,140,571)
    if xy is not None:
        adb.touch(xy)
    #if (f.find(IMAGE_BASE_FRIEND,False)[2]>0.5):
    #    adb.touch(f.find(IMAGE_BASE_FRIEND,False))
    time.sleep(4)
    adb.touch((160,60))
    time.sleep(5)
    if not ready.is_main_menu() :
        raise RuntimeError('发现角色对话，请自行解决。')

