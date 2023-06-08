import os;

def get_screen_shot():
    Path = os.getcwd().replace("\\",'/')
    # print(f"{Path}/screenshot.png")
    os.system("adb shell screencap /sdcard/screenshot.png")
    # print(f"{Path}/screenshot.png")
    os.system(f"adb pull /sdcard/screenshot.png {Path}\screenshot.png")
    # print(f"{Path}/screenshot.png")
    ans = os.system("adb shell rm /sdcard/screenshot.png")
