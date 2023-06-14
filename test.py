import cv2 as cv
import numpy as np
import lib.find as f

def match_icon(image, icon):
    img = cv.imread(image)
    # 读取透明背景的图标，并转换成灰度图像
    template = cv.imread(icon,cv.IMREAD_UNCHANGED)
    template2 = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

    # 分离alpha通道，作为模板匹配的掩码
    channels = cv.split(template)
    mask = np.array(channels[3])

    # 转换RGB图像为灰度图像
    img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # 根据alpha通道的值，设置掩码的值
    mask[channels[3] == 0] = 1
    mask[channels[3] == 100] = 0

    # 使用cv2.TM_SQDIFF方法进行模板匹配，并传入掩码参数
    method = cv.TM_SQDIFF  
    result = cv.matchTemplate(img, template2, method, mask=mask)
    # 获取匹配结果的最小值、最大值、最小位置和最大位置
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    # 计算目标中心点的坐标
    target_center = (min_loc[0] + template.shape[1] // 2, min_loc[1] + template.shape[0] // 2)

    # 计算相似度
    similarity = 1- min_val
    threshold = 0.6  # 阈值
    loc = np.where(result >= threshold)
    print(loc)
    if len(loc[0]) > 0:
        return loc[1][0], loc[0][0]
    return target_center, similarity


print(match_icon('cache/test.png', 'imgs/go_back_2.png'))
img = cv.imread("cache/test.png")
img_terminal = cv.imread(f'imgs/go_back_2.png')

# print(img_terminal.shape)
height, width, dep = img_terminal.shape

result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)

upper_left = cv.minMaxLoc(result)[2]
img2 = img[upper_left[1]:upper_left[1]+height,
            upper_left[0]:upper_left[0] + width]
lower_right = (upper_left[0]+width, upper_left[1]+height)

avg = (int((upper_left[0]+lower_right[0])/2),
        int((upper_left[1]+lower_right[1])/2),
        f.similar(img_terminal, img2))
print(avg)
