from config.config import data
import lib.adb_command as adb
import lib.api as api
# import cv2 as cv
import time 
import lib.find as f
# import os
# import plugins.Turn as Turn
# import plugins.auto_battle as auto
# import decisions.decision_1 as de1
import plugins.active as active
# import plugins.wilderness as wilderness
# import plugins.mission as mission
import plugins.path as path
import config.config as config
import lib.ppocr as pp
"""
print('开始初始化adb')
device = adb.is_device_connected()
if not device:
    print("Error: 未连接设备，请回看上面的错误信息")
    exit(1)
#检测游戏是否运行，如果没有运行就启动游戏
adb.is_game_on()
#进入主菜单
path.to_menu()
"""
print(pp.ocr_cn('cache/screenshot.png'))
#active.Auto_Active(LEVEL_6,)
#adb.touch(f.find('imgs/enter_the_show'))
#print("正在进入主会场")
#time.sleep(1)

"""
def match_icon(image, icon):
    image = cv.imread(image)
    # 读取透明背景的图标，并转换成无符号8位整数类型
    template = cv.imread(icon,cv.IMREAD_UNCHANGED)
    template = np.uint8(template)

    # 分离alpha通道，作为模板匹配的掩码
    channels = cv.split(template)
    mask = np.array(channels[3])

    # 根据alpha通道的值，设置掩码的值
    mask[channels[3] == 0] = 1
    mask[channels[3] == 100] = 0

    # 使用cv2.TM_SQDIFF方法进行模板匹配，并传入掩码参数
    method = cv.TM_SQDIFF  

    # 初始化一个空列表，用于存放每个通道和灰度图像的匹配结果
    results = []

    # 对每个通道和灰度图像进行模板匹配，并把结果添加到列表中
    for i in range(4):
    # 如果是第四个通道，就把图像转换成灰度图像
        if i == 3:
            img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            temp = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
        # 否则就取对应的通道
        else:
            img = image[:,:,i]
            temp = template[:,:,i]
        # 进行模板匹配，并获取最小值、最大值、最小位置和最大位置
        result = cv.matchTemplate(img, temp, method, mask=mask)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # 计算目标中心点的坐标
        target_center = (max_loc[0] + temp.shape[1] / 2, max_loc[1] + temp.shape[0] / 2)
        # 把坐标和相似度作为元组添加到列表中
        results.append((target_center, max_val))
        print(max_val,max_loc)
print(match_icon('cache/test.png', 'imgs/go_back_2_alpha.png'))
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
"""