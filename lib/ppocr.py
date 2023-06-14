import os
from lib.OCR.api import GetOcrApi
#config_path是相对于PaddleOCR-json.exe的路径
argument_cn = {'config_path': "models/config_chinese.txt"}
argument_en = {'config_path': "models/config_en.txt"}
current_path = os.path.abspath(os.path.dirname(__file__))
project_path = os.path.dirname(current_path)
exe_path=current_path+"\OCR\PaddleOCR-json.exe"
print(exe_path)

def ocr_cn(target):
    target_path =os.path.join(project_path, target.replace('/', '\\'))
    ocr = GetOcrApi(exe_path, argument_cn)
    res = ocr.run(target_path)
    return res

def ocr_xy(target):
    
    print('还没写')


def ocr_en(target):
    target_path =os.path.join(project_path, target.replace('/', '\\'))
    ocr2 = GetOcrApi(exe_path, argument_en)
    res = ocr2.run(target_path)

    return res