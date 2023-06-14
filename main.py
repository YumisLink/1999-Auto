from config.config import data
import lib.adb_command as adb
import lib.api as api
# import cv2 as cv
# from time import sleep
# import lib.find as f
# import os
# import plugins.Turn as Turn
# import plugins.auto_battle as auto
# import decisions.decision_1 as de1
# import plugins.active as active
# import plugins.wilderness as wilderness
# import plugins.mission as mission

# from config.mappoint import clickcard
# import time

# from cnocr import CnOcr




def init():
    device = adb.is_device_connected()
    if not device:
        print("Error: 未连接设备，请回看上面的错误信息")
        exit(1)
    adb.is_game_on()
    api.get_screen_shot()
    # img = cv.imread("cache/screenshot.png")
    # height, width, dep = img.shape
    # data['x'] = height
    # data['y'] = width


init()

# 这里是mumu12的连接，如果你用的不是mumu12请去看看你的模拟器使用的是哪个adb调试端口。
# t = Turn()
# t.team = ['Anan', 'Bkornblume', 'Eternity']
# checkTurn(t)







# wilderness.wild_start()
# active.Auto_Active(active.IMAGE_ANALYSIS, active.LEVEL_5, active.REPLAY_2)
# active.Auto_Active(active.IMAGE_MINTAGE_AESTHETICS, active.LEVEL_6, active.REPLAY_2)
# active.Auto_Active(active.IMAGE_THE_POUSSIERE, active.LEVEL_6, active.REPLAY_2)
# mission.mission_start()


#t = Turn.Turn()
#t.team = ['Eternity','Anan','Sotheby','Bkornblume']

# print(f.search_cards(t.team))
#auto.checkTurn(t)


