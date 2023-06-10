import find as f
import time
import adb_command
import api


def ready():
    cnt = 0
    # a = f.find('imgs/main_menu_checker')
    # print(a)
    # if (a[2] > 0.75):
    #     return True
    # goback = f.find('imgs/back_to_menu')
    # print(goback)
    # if (goback[2] > 0.7):
    #     adb_command.touch(goback)
    # time.sleep(1.2)
    # a = f.find('imgs/main_menu_checker')
    # if (a[2] > 0.75):
    #     return True
    while(True):
        cnt += 1
        a = f.find('imgs/main_menu_checker')
        if (a[2] > 0.75):
            return True
        adb_command.touch((100, 60))
        time.sleep(0.4)
        # goback = f.find('imgs/go_back_1', False)
        # if goback[2] > 0.6:
        #     adb_command.touch(goback)
        # goback = f.find('imgs/go_back_2', False)
        # if goback[2] > 0.6:
        #     adb_command.touch(goback)
        # goback = f.find('imgs/go_back_3', False)
        # if goback[2] > 0.6:
        #     adb_command.touch(goback)
        if cnt >= 15:
            return False


# if not ready():
#     print("error")
    # adb_command.touch(f.find('imgs/back_to_menu'))
