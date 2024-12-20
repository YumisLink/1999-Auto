from lib import ppocr

if __name__ == "__main__":
    res = ppocr.ocr_cn("imgs/mission_week.png")
    print(res)