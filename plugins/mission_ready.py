import lib.find as f
import time
import lib.adb_command as adb


def ready():
    cnt = 0
    while(True):
        cnt += 1
        a = f.find('imgs/main_menu_checker')
        if (a[2] > 0.75):
            return True
        adb.touch((60, 60))
        time.sleep(0.6)
        if cnt >= 15:
            return False

def is_main_menu():
    a = f.find('imgs/main_menu_checker')
    if (a[2] > 0.75):
        return True
    return False

