import adb_command as adb
import api
from time import sleep
from find import find, similar, search_cards, read_screenshot
from config.config import data
import cv2 as cv
import os
import active as play


def init():
    api.get_screen_shot()
    img = read_screenshot()
    height, width, dep = img.shape
    data['x'] = height
    data['y'] = width

# 这里是mumu12的连接，如果你用的不是mumu12请去看看你的模拟器使用的是哪个adb调试端口。
# os.system("adb connect 127.0.0.1:16384")
# t = Turn()
# t.team = ['Anan', 'Bkornblume', 'Eternity']
# checkTurn(t)


# img = cv.imread('screenshot.png')
# img_terminal = cv.imread('head.png')
# result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)
# print(result)
# print(1)

init()
play.Auto_Active(play.IMAGE_MINTAGE_AESTHEICS, play.LEVEL_6, play.REPLAY_2)
play.Auto_Active(play.IMAGE_THE_POUSSIERE, play.LEVEL_6, play.REPLAY_1)


# while(True):
#     adb.touch((data['y']/15, data['x']/15))
#     sleep(0.1)

# while(True):
#     adb.touch((data['y']-50, data['x']/5*4))
# adb.swipe((data['y']-50, data['x']/5*4), (50, data['x']/5*4))

# sleep(0.25)
# a = find('imgs/friends')
# if (a[2] > 0.65):
#     touch(a[0], a[1])
# sleep(0.25)
# a = find('imgs/money')
# if (a[2] > 0.65):
#     touch(a[0], a[1])
# sleep(0.25)
# print(a)
# while(True):
# touch(a[0], a[1])
# find('123')
# find('bs')

# touch(click[0],click[1])
