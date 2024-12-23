from lib import ppocr
from lib import adb_command as adb
from lib import api

if __name__ == "__main__":
    res = ppocr.ocr_cn("imgs/mission_week.png")
    print(res)

    if adb.fast_check_connected():
        print("device connected, test on current screen")
        img = api.get_screen_shot()
        res = ppocr.ocr_cn(img)
        print(res)

        # import cv2
        # img = cv2.imread('cache/screenshot.png')
        # img = img[675: 767, 682: 859, :]
        # res = ppocr.ocr_bytes_cn(img)
        # print(res)