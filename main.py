from abd_command import touch
from find import find, similar, search_cards
from Turn import Turn, checkTurn
import os

# 这里是mumu12的连接，如果你用的不是mumu12请去看看你的模拟器使用的是哪个adb调试端口。
os.system("adb connect 127.0.0.1:16384")
t = Turn()
t.team = ['Anan', 'Bkornblume', 'Eternity']
checkTurn(t)


# touch(click[0],click[1])

# adb shell screencap /sdcard/app.png
# adb pull /sdcard/app.png E:\Netease\app.png
# adb shell rm /sdcard/app.png
