import sys
import cv2

from lib import adb_command as adb
from lib import api

def shot(cut: list[int] = None):
    assert adb.is_device_connected()
    fname = api.get_screen_shot()
    img = cv2.imread(fname)
    if cut:
        img = img[cut[0]:cut[1], cut[2]:cut[3]]
    cv2.imshow('shot', img)
    cv2.waitKey(0)
    cv2.imwrite('shot.png', img)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        y1, y2, x1, x2 = sys.argv[1:]
        cut = [int(y1), int(y2), int(x1), int(x2)]
    else:
        cut = None
        
    shot(cut)