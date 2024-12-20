import os
import numpy as np
import cv2 as cv
from loguru import logger

try:
    if os.name == 'nt':
        from lib.OCR_Windows.api import GetOcrApi
    else:
        from lib.OCR_Linux.api import GetOcrApi
except Exception:
    logger.critical(
        "请从 https://github.com/hiroi-sora/PaddleOCR-json/releases/tag/v1.4.1"
        "下载当前系统对应版本发布包并解压至 lib/OCR_Windows 或 lib/OCR_Linux"
    )
    raise ImportError("OCR模块导入失败")

#config_path是相对于PaddleOCR-json.exe的路径
argument_cn = {'config_path': "models/config_chinese.txt"}
argument_en = {'config_path': "models/config_en.txt"}
current_path = os.path.abspath(os.path.dirname(__file__))
project_path = os.path.dirname(current_path)
# exe_path=current_path+"\\OCR\\PaddleOCR-json.exe"

if os.name == 'nt':
    exe_path = os.path.join(current_path, r'OCR_Windows/PaddleOCR-json.exe')
else:
    exe_path = os.path.join(current_path, r'OCR_Linux/run.sh')

#输出结果文档：https://github.com/hiroi-sora/PaddleOCR-json/tree/main#readme
#API文档：https://github.com/hiroi-sora/PaddleOCR-json/tree/main/api/python

#启动时初始化
#ocr = GetOcrApi(exe_path, argument_cn)
#ocr2 = GetOcrApi(exe_path, argument_en)
ocr_cn_engine = None
def ocr_cn(target):
    target_path =os.path.join(project_path, target)
    global ocr_cn_engine
    if ocr_cn_engine is None:
        ocr_cn_engine = GetOcrApi(exe_path, argument=argument_cn)
    res = ocr_cn_engine.run(target_path)
    return res
ocr_en_engine = None
def ocr_en(target):
    target_path =os.path.join(project_path, target)
    global ocr_en_engine
    if ocr_en_engine is None:
        ocr_en_engine = GetOcrApi(exe_path, argument=argument_en)
    res = ocr_en_engine.run(target_path)

    return res

def ocr_xy(target,text='',cn=True):
    """
    识别target图片中包含text的区域，返回中心坐标
    :param target:需要识别图片的路径.
    :param text:预期文本.
    :param cn:是否使用中文ocr.
    :Return: 中心坐标、识别文本和匹配度.
    """
    if cn:
        res=match_text_area(ocr_cn(target), text)
    else:
        res=match_text_area(ocr_en(target), text)
    return res

def ocr_bytes_cn(imagebytes):
    #直接传入图片字节流有问题处理不了，先存到本地再识别（先用着，将来可能会修吧）
    cv.imwrite('cache/ocr_bytes_cn.png', imagebytes)
    res=ocr_cn('cache/ocr_bytes_cn.png')
    return res

def ocr_bytes_en(imagebytes):
    cv.imwrite('cache/ocr_bytes_en.png', imagebytes)
    res=ocr_cn('cache/ocr_bytes_en.png')
    return res

def ocr_bytes_xy(imagebytes,text='',cn=True):
    """
    识别target图片中包含text的区域，返回中心坐标
    :param imagebytes:需要识别的图片字节流.
    :param text:预期文本.
    :param cn:是否使用中文ocr.
    :Return: 中心坐标、识别文本和匹配度.
    """
    if cn:
        res=match_text_area(ocr_bytes_cn(imagebytes), text)
    else:
        res=match_text_area(ocr_bytes_en(imagebytes), text)
    return res

def cut_ocr_bytes(imagebytes,x,y,w,h,is_cn=True):
    """
    OCR识别裁切区域
    :param imagebytes:需要识别的图片字节流.
    :param x: 指定区域左上角的横坐标
    :param y: 指定区域左上角的纵坐标
    :param w: 指定区域的宽度
    :param h: 指定区域的高度
    :param is_cn:是否使用中文ocr.
    :Return: {"code": 识别码, "data": 内容列表或错误信息字符串}.
    """
    img_cut=imagebytes[y:y+h,x:x+w]
    if is_cn:
        res=ocr_bytes_cn(img_cut)
    else:
        res=ocr_bytes_en(img_cut)
    return res

def cut_html_ocr_bytes(imagebytes,x1,y1,x2,y2,is_cn=True):
    # 用于处理从 https://www.image-map.net 框出来的坐标
    """
    OCR识别裁切区域
    :param imagebytes:需要识别的图片字节流.
    :param x1: 指定区域的某个横坐标
    :param y1: 指定区域的某个的纵坐标
    :param x2: 指定区域的某个横坐标
    :param y2: 指定区域的某个的纵坐标
    :param is_cn:是否使用中文ocr.
    :Return: {"code": 识别码, "data": 内容列表或错误信息字符串}.
    """
    if x2 < x1:
        a = x2
        x2 = x1
        x1 = a
    if y2 < y1:
        a = y2
        y2 = y1
        y1 = a
    img_cut=imagebytes[y1:y2,x1:x2]
    if is_cn:
        res=ocr_bytes_cn(img_cut)
    else:
        res=ocr_bytes_en(img_cut)
    return res

def cut_html_ocr_bytes_xy(imagebytes,x1,y1,x2,y2,text='',is_cn=True):
    # 用于处理从 https://www.image-map.net 框出来的坐标
    """
    识别target图片中包含text的区域，返回中心坐标
    :param imagebytes:需要识别的图片字节流.
    :param x1: 指定区域的某个横坐标
    :param y1: 指定区域的某个的纵坐标
    :param x2: 指定区域的某个横坐标
    :param y2: 指定区域的某个的纵坐标
    :param text:预期文本.
    :param cn:是否使用中文ocr.
    :Return: 中心坐标、识别文本和匹配度.
    """
    if x2 < x1:
        a = x2
        x2 = x1
        x1 = a
    if y2 < y1:
        a = y2
        y2 = y1
        y1 = a
    img_cut=imagebytes[y1:y2,x1:x2]
    if is_cn:
        out=ocr_bytes_cn(img_cut)
    else:
        out=ocr_bytes_en(img_cut)
    
    # if is_char_by_char:
    #     res=match_text_area_char_by_char(out, text)
    # else:
    #     res=match_text_area(out, text)
    res=match_text_area(out, text)
    if res[0] is None:
        logger.debug('未识别到目标文本')
        return None,None,None
    result=res
    result[0][0]=res[0][0]+x1
    result[0][1]=res[0][1]+y1
    return result
    

def match_text_area(res, text):
    #这个是中间函数，不要直接调用，请用ocr_xy
    """
    在返回中筛选出包含text的区域，如果有多个区域，选择最接近中心的区域 返回其中心坐标和相似度
    :param res:返回的字典.
    :param text:预期文本.
    :Return: 中心坐标x、y、识别文本和匹配度.
    """
    if res['code'] != 100:
        logger.debug(res)
        return None, None, None, None
    match_areas = []
    similarities = []
    texts = []
    for item in res['data']:
        if text in item['text']:
            match_areas.append(item['box'])
            similarities.append(item['score'])
            texts.append(item['text'])
    if len(match_areas) == 0:
        logger.debug(res['data'])
        return None, None, None, None
    if len(match_areas) == 1:
        center = np.mean(match_areas[0], axis=0)
        return center.tolist(), similarities[0], texts[0]
    # 如果有多个匹配区域，选择最接近中心的区域
    centers = []
    for area in match_areas:
        center = np.mean(area, axis=0)
        centers.append(center)
    centers = np.array(centers)
    distances = np.linalg.norm(centers - np.array(res['image_size']) / 2, axis=1)
    min_idx = np.argmin(distances)
    return centers[min_idx].tolist(), texts[min_idx], similarities[min_idx]

def match_text_area_char_by_char(res, text):
    """
    在返回中筛选出包含text(和text的一部分)的区域，如果有多个区域，选择最接近中心的区域 返回其中心坐标和相似度
    :param res:返回的字典.
    :param text:预期文本.
    :Return: 中心坐标x、y、识别文本和匹配度.
    """
    if res['code'] != 100:
        logger.debug(res)
        return None, None, None, None
    match_areas = []
    similarities = []
    texts = []
    for item in res['data']:
        if all(char in item['text'] for char in text):
            match_areas.append(item['box'])
            similarities.append(item['score'])
            texts.append(item['text'])
    if len(match_areas) == 0:
        return None, None, None, None
    if len(match_areas) == 1:
        center = np.mean(match_areas[0], axis=0)
        return center.tolist(), similarities[0], texts[0]
    # 如果有多个匹配区域，选择最接近中心的区域
    centers = []
    for area in match_areas:
        center = np.mean(area, axis=0)
        centers.append(center)
    centers = np.array(centers)
    distances = np.linalg.norm(centers - np.array((1600, 900)) / 2, axis=1)#TODO:兼容更多屏幕分辨率
    min_idx = np.argmin(distances)
    return centers[min_idx].tolist(), texts[min_idx], similarities[min_idx]