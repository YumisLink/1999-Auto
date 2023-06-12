import cv2 as cv
import lib.api as api
from cards.aname import card_reflect


def read_screenshot():
    img = cv.imread("screenshot.png")
    return img

def find_image(id: str, take=True):
    if take:
        api.get_screen_shot()
    img = cv.imread("screenshot.png")
    img_terminal = cv.imread(f'{id}.png')

    # print(img_terminal.shape)
    height, width, dep = img_terminal.shape

    result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)

    upper_left = cv.minMaxLoc(result)[2]
    img = cv.imread("screenshot.png")
    img2 = img[upper_left[1]:upper_left[1]+height,
               upper_left[0]:upper_left[0] + width]
    return img2

def find(id: str, take=True):
    if take:
        api.get_screen_shot()
    img = cv.imread("screenshot.png")
    img_terminal = cv.imread(f'{id}.png')

    # print(img_terminal.shape)
    height, width, dep = img_terminal.shape

    result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)

    upper_left = cv.minMaxLoc(result)[2]
    img = cv.imread("screenshot.png")
    img2 = img[upper_left[1]:upper_left[1]+height,
               upper_left[0]:upper_left[0] + width]
    lower_right = (upper_left[0]+width, upper_left[1]+height)

    avg = (int((upper_left[0]+lower_right[0])/2),
           int((upper_left[1]+lower_right[1])/2),
           similar(img_terminal, img2))
    # cv.imwrite(f'{id}2.png', img2)
    return avg


def search_cards(character: list):
    img = cv.imread("screenshot.png")
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
# img  = cv.imread("screenshot.png")
# x = 190
# y = 778
# img = img[x:118,y:85]
# checker = cv.imread("cards/disappear.png")
# print(calculate(checker,img))
