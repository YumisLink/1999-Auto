import os
import cv2 as cv
import api 
import math
from cards.aname import card_reflect

def find(id:str):
    api.get_screen_shot()
    img  = cv.imread("screenshot.png")
    img_terminal = cv.imread(f'{id}.png')

    print(img_terminal.shape)
    height, width,dep = img_terminal.shape

    result = cv.matchTemplate(img,img_terminal,cv.TM_SQDIFF_NORMED)


    upper_left = cv.minMaxLoc(result)[2]
    lower_right = (upper_left[0]+width,upper_left[1]+height)

    print(cv.minMaxLoc(result))


    avg = (int((upper_left[0]+lower_right[0])/2),int((upper_left[1]+lower_right[1])/2))

    return avg

def search_cards():
    img  = cv.imread("screenshot.png")
    x = 687
    y = 520
    ls = []
    for i in range(0,7):
        ls.append(img[x:x+180,y+i*154:y+140+i*154])
        # cv.imwrite(f'{i}.png',img2)
    character = ['Anan','Bkornblume','Eternity']
    characters = []
    for i in range(0,3):
        characters.append(f'{character[i]}1')
        characters.append(f'{character[i]}2')
        characters.append(f'{character[i]}3')
    characters.append('None')
    ccard =[]
    for i in range(0,9):
        ccard.append(cv.imread(f'cards/{characters[i]}.png'))

    cards = []
    # print(card_reflect['Anan1'])
    for i in range(0,7):
        best = 0
        target = 9
        for j in range(0,9):
            best = similar(ccard[j],ls[i])
            if best>0.58 :
                target = j
                break
        cards.append(card_reflect[f'{characters[target]}'])
    print(cards)
    return cards







def calculate(image1, image2):
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

def similar(image1,image2,size=(160,210)):
    image1 = cv.resize(image1, size)
    image2 = cv.resize(image2, size)
    sub_image1 = cv.split(image1)
    sub_image2 = cv.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data





api.get_screen_shot()
img  = cv.imread("screenshot.png")
x = 190
y = 778
img = img[x:118,y:85]
checker = cv.imread("cards/disappear.png")
print(calculate(checker,img))