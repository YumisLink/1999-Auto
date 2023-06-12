from time import sleep
import lib.api as api
import lib.find as f
from config.config import data
import cv2 as cv
import os
import lib.adb_command as adb
import plugins.Turn as Turn
import plugins.auto_battle as auto
import decisions.decision_1 as de1
import plugins.active as active
import plugins.wilderness as wilderness
import plugins.mission as mission

from config.mappoint import clickcard
import time

from cnocr import CnOcr


def init():
    api.get_screen_shot()
    img = cv.imread("screenshot.png")
    height, width, dep = img.shape
    data['x'] = height
    data['y'] = width

# 这里是mumu12的连接，如果你用的不是mumu12请去看看你的模拟器使用的是哪个adb调试端口。
# t = Turn()
# t.team = ['Anan', 'Bkornblume', 'Eternity']
# checkTurn(t)


# img = cv.imread('screenshot.png')
# img_terminal = cv.imread('head.png')
# result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)
# print(result)
# print(1)



# os.system("adb connect 127.0.0.1:16384")
# init()

# wilderness.wild_start()
# active.Auto_Active(active.IMAGE_ANALYSIS, active.LEVEL_5, active.REPLAY_2)
# active.Auto_Active(active.IMAGE_MINTAGE_AESTHETICS, active.LEVEL_6, active.REPLAY_2)
# active.Auto_Active(active.IMAGE_THE_POUSSIERE, active.LEVEL_6, active.REPLAY_2)
# mission.mission_start()


t = Turn.Turn()
t.team = ['Eternity','Anan','Sotheby','Bkornblume']

# print(f.search_cards(t.team))
auto.checkTurn(t)


# t.card = f.search_cards(t.team)
# t.buff = 1
# print(t.card)
# d = de1.normal_cards_upgrade(t)
# print(d[0])
# adb.touch(clickcard[d[0][0]])
# time.sleep(d[0][1])
# print(d[1])
# adb.touch(clickcard[d[1][0]])
# time.sleep(d[1][1])
# print(d[2])
# adb.touch(clickcard[d[2][0]])