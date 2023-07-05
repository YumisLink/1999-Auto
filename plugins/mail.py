import time
import lib.adb_command as adb
import plugins.path as path

def mail_start():
    path.to_menu()
    adb.touch([98,230])
    time.sleep(1)
    adb.touch([263,770])
    time.sleep(1)
    path.to_menu()