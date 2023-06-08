import os;
from config.mappoint import clickcard

def touch(x,y):
    print(f'click {x} {y}')
    print(os.system(f'adb shell input tap {x} {y}'))

# while(True):
#     touch(clickcard[0][1],clickcard[0][0])

