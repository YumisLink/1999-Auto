from config.config import data,check_path
import lib.adb_command as adb
import lib.api as api
import plugins.active as active
import lib.find as f
import plugins.Turn as Turn
import plugins.auto_battle as auto
# import cv2 as cv
# from time import sleep
# import os
# import decisions.decision_1 as de1
# import plugins.wilderness as wilderness
# import plugins.mission as mission
#import plugins.path as path

# from config.mappoint import clickcard
# import time




def init():
    #adb初始化
    check_path()
    device = adb.is_device_connected()
    if not device:
        print("Error: 未连接设备，请回看上面的错误信息")
        exit(1)
    #检测游戏是否运行，如果没有运行就启动游戏
    adb.is_game_on()
    api.get_screen_shot()


init()

# 自动收菜把下面的注释取消掉就可以运行：

# wilderness.wild_start()
active.Auto_Active(active.IMAGE_ANALYSIS, active.LEVEL_5, active.REPLAY_2)  # 圣遗物狗粮本 等级5 复现2
active.Auto_Active(active.IMAGE_MINTAGE_AESTHETICS, active.LEVEL_6, active.REPLAY_2)# 钱本 等级6 复现2
active.Auto_Active(active.IMAGE_THE_POUSSIERE, active.LEVEL_6, active.REPLAY_2)# 经验本 等级6 复现2
# mission.mission_start()



# 自动战斗：


# t = Turn.Turn()
# t.team = ['Eternity','Anan','Sotheby','Bkornblume']   #这里是你的角色名，请去 cards/aname.py 对照英文填写，可以多写把你常用的角色加入。
# auto.checkTurn(t)











