import os
import numpy as np
import cv2 as cv
from lib.OCR.api import GetOcrApi
#config_path是相对于PaddleOCR-json.exe的路径
argument_cn = {'config_path': "models/config_chinese.txt"}
argument_en = {'config_path': "models/config_en.txt"}
current_path = os.path.abspath(os.path.dirname(__file__))
project_path = os.path.dirname(current_path)
exe_path=current_path+"\\OCR\\PaddleOCR-json.exe"
#print(exe_path)
#文档：https://github.com/hiroi-sora/PaddleOCR-json/tree/main/api/python

#启动时初始化
ocr = GetOcrApi(exe_path, argument_cn)
#ocr2 = GetOcrApi(exe_path, argument_en)

def ocr_cn(target):
    target_path =os.path.join(project_path, target.replace('/', '\\'))
    #ocr = GetOcrApi(exe_path, argument_cn)
    res = ocr.run(target_path)
    return res

def ocr_en(target):
    target_path =os.path.join(project_path, target.replace('/', '\\'))
    ocr2 = GetOcrApi(exe_path, argument_en)
    res = ocr2.run(target_path)

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



def match_text_area(res, text):
    """
    在返回中筛选出包含text的区域，如果有多个区域，选择最接近中心的区域 返回其中心坐标和相似度
    :param res:返回的字典.
    :param text:预期文本.
    :Return: 中心坐标x、y、识别文本和匹配度.
    """
    if res['code'] != 100:
        print(res)
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
        print(res)
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
    distances = np.linalg.norm(centers - np.array(res['image_size']) / 2, axis=1)
    min_idx = np.argmin(distances)
    return centers[min_idx].tolist(), texts[min_idx], similarities[min_idx]