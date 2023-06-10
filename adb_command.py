import os
from config.mappoint import clickcard


def touch(x, y):
    print(f'click {x} {y}')
    print(os.system(f'adb shell input tap {x} {y}'))


def touch(point):
    print(f'click {point[0]} {point[1]}')
    print(os.system(f'adb shell input tap {point[0]} {point[1]}'))


def swipe(p1, p2):
    print(f'swipe from  {p1[0]} {p1[1]} to {p2[0]} {p2[1]}')
    print(
        os.system(f'adb shell input touchscreen swipe {p1[0]} {p1[1]} {p2[0]} {p2[1]} 100'))
