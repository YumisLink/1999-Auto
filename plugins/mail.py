import time
import lib.adb_command as adb
import plugins.path as path

def mail_start():
    if not path.to_menu():
        return False
    adb.touch([98,230])
    time.sleep(1)
    adb.touch([263,770])
    time.sleep(1)
    return path.to_menu()