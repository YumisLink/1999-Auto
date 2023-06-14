import cv2 as cv
import numpy as np 
import lib.api as api
from cards.aname import card_reflect


def read_screenshot():
    img = cv.imread("cache/cache/screenshot.png")
    return img

def find_image(id: str, take=True):
    """
    从id中匹配图片并返回其在截图中的样子
    :param id:图片的id.
    :param take:图片要不要现截.
    :Return: img2:找到的图片
    """
    if take:
        api.get_screen_shot()
    img = cv.imread("cache/screenshot.png")
    img_terminal = cv.imread(f'{id}.png')

    # print(img_terminal.shape)
    height, width, dep = img_terminal.shape

    result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)
    upper_left = cv.minMaxLoc(result)[2]
    img2 = img[upper_left[1]:upper_left[1]+height,
               upper_left[0]:upper_left[0] + width]
    return img2

def find(id: str, take=True):
    """
    从id中匹配图片并返回其中心点的xy坐标及匹配度
    :param id:图片的id.
    :param take:图片要不要现截.
    :Return: avg:找到的图片的中心点坐标，以及相似度
    """
    if take:
        api.get_screen_shot()
    img = cv.imread("cache/screenshot.png")
    img_terminal = cv.imread(f'{id}.png')

    # print(img_terminal.shape)
    height, width, dep = img_terminal.shape

    result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)

    upper_left = cv.minMaxLoc(result)[2]
    img2 = img[upper_left[1]:upper_left[1]+height,
               upper_left[0]:upper_left[0] + width]
    lower_right = (upper_left[0]+width, upper_left[1]+height)

    avg = (int((upper_left[0]+lower_right[0])/2),
           int((upper_left[1]+lower_right[1])/2),
           similar(img_terminal, img2))
    # cv.imwrite(f'cache/{id}2.png', img2)
    return avg

#裁屏匹配
def cut_find(template, x, y, w, h,take=True):
    """
    识别截图中指定区域的目标坐标
    :param template: 模板图片
    :param x: 指定区域左上角的横坐标
    :param y: 指定区域左上角的纵坐标
    :param w: 指定区域的宽度
    :param h: 指定区域的高度
    :take: 是否截图
    :return x,y:返回的坐标
    """
    if take:
        api.get_screen_shot()
    screen = cv.imread("cache/screenshot.png")
    template_img = cv.imread(template)
    screen_cut = screen[y:y+h, x:x+w]
    result = cv.matchTemplate(screen_cut , template_img, cv.TM_SQDIFF_NORMED)
    threshold = 0.6  # 阈值
    loc = np.where(result >= threshold)
    if len(loc[0]) > 0:
        # 在匹配结果上画框
        for pt in zip(*loc[::-1]):
            cv.rectangle(screen_cut, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv.imwrite('cache/result2.png', screen_cut)
        x=loc[1][0]+x 
        y=loc[0][0]+y
        return x, y
    else:
        print('匹配度过低'+ str(result))
        return None

def cut_find_html(template, x2, y2, x1, y1,take=True):
    """
    识别截图中指定区域的目标坐标
    :param template: 模板图片
    :param x1: 指定区域的某个横坐标
    :param y1: 指定区域的某个的纵坐标
    :param x2: 指定区域的某个横坐标
    :param y2: 指定区域的某个的纵坐标
    :take: 是否截图
    :return x,y:返回的坐标
    """
    #用于处理从 https://www.image-map.net 框出来的坐标
    if x2<x1:
        a=x2
        x2=x1
        x1=a
    if y2<y1:
        a=y2
        y2=y1
        y1=a
    w=x2-x1
    h=y2-y1
    cut_find(template, x1, y1, w, h,take)


def search_cards(character: list):
    img = cv.imread("cache/screenshot.png")
    x = 687
    y = 520
    ls = []
    star = []
    for i in range(0, 7):
        finally_y = y+i*154

        star_x = x-15
        s = 0
        ls.append(img[x:x+180, finally_y:finally_y+140])
        cut = img[star_x:star_x+1+3, finally_y+39:finally_y+40+5]
        # print(f'{i} 1:{cut[0][0][2]}')
        if cut[0][0][2] > 200:
            s = 1
        # cv.imwrite(f'{i}star1.png',cut)
        cut = img[star_x:star_x+1+3, finally_y+80:finally_y+80+5]
        # print(f'{i} 2:{cut[0][0][2]}')
        if cut[0][0][2] > 200:
            s = 2
        # cv.imwrite(f'{i}star2.png',cut)
        cut = img[star_x:star_x+1+3, finally_y+100:finally_y+100+5]
        # print(f'{i} 3:{cut[0][0][2]}')
        if cut[0][0][2] > 200:
            s = 3
        # cv.imwrite(f'{i}star3.png',cut)
        star.append(s)

    characters = []
    for chars in character:
        characters.append(f'{chars}1')
        characters.append(f'{chars}2')
        characters.append(f'{chars}3')
    characters.append('None')
    ccard = []
    for i in characters:
        ccard.append(cv.imread(f'cards/{i}.png'))

    cards = []
    for i in range(0, 7):
        best = 0
        target = len(ccard)-1
        sim_val = 0
        for j in range(0,len(ccard)-1):
            best = similar(ccard[j], ls[i])
            # print(f'{i} and {characters[j]} sim = {best}')
            if best > sim_val and best > 0.55:
                target = j
                sim_val = best
                # break
        cards.append((card_reflect[f'{characters[target]}'], star[i]))
    # print(cards)
    return cards


def calculate(image1, image2):
    """
    用灰度直方图计算图片相似度
    :param image1:用来比较的图1.
    :param image2:用来比较的图2.
    :Return: degree:重合度
    """
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def similar(image1, image2, size=(160, 210)):
    """
    用三通道灰度直方相似度平均值计算图片相似度
    :param image1:用来比较的图1.
    :param image2:用来比较的图2.
    :param size:重缩放的大小.
    :Return: degree:重合度
    """    
    image1 = cv.resize(image1, size)
    image2 = cv.resize(image2, size)
    sub_image1 = cv.split(image1)
    sub_image2 = cv.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


# api.get_screen_shot()
# print(search_cards(['Anan', 'Bkornblume', 'Eternity']))
# img  = cv.imread("cache/screenshot.png")
# x = 190
# y = 778
# img = img[x:118,y:85]
# checker = cv.imread("cards/disappear.png")
# print(calculate(checker,img))
