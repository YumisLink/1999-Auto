import os;
from config.mappoint import clickcard

def touch(x,y):
    print(f'click {x} {y}')
    print(os.system(f'adb shell input tap {x} {y}'))

