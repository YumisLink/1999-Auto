#from config.config import data
import lib.adb_command as adb
#import lib.api as api
#import cv2 as cv
import time 
import lib.find as f
# import os
# import plugins.Turn as Turn
# import plugins.auto_battle as auto
# import decisions.decision_1 as de1
import plugins.active as active
import plugins.wilderness as wilderness
import plugins.mission as mission
import plugins.autopass as autopass
import plugins.path as path
#import config.config as config
#import lib.ppocr as pp

TIMES_A_DAY=2#一天几次
START_TIME='04:02'#从几点开始

print('开始初始化adb')
device = adb.is_device_connected()
if not device:
    print("Error: 未连接设备，请回看上面的错误信息")
    exit(1)

while True:
    # 获取当前时间
    now = time.localtime()
    # 计算今天的 START_TIME 时间点
    start_time = time.strptime(START_TIME, '%H:%M')
    today_start_time = time.struct_time((now.tm_year, now.tm_mon, now.tm_mday, start_time.tm_hour, start_time.tm_min, 0, 0, 0, now.tm_isdst))
    today_start_time_seconds = time.mktime(today_start_time)
    # 计算下一次执行时间
    if now.tm_sec >= start_time.tm_sec:
        next_run_time_seconds = today_start_time_seconds + (TIMES_A_DAY - 1) * 24 * 3600 / TIMES_A_DAY
    else:
        next_run_time_seconds = today_start_time_seconds
    while time.time() >= next_run_time_seconds:
        next_run_time_seconds += 24 * 3600 / TIMES_A_DAY
    # 计算下一次执行时间与当前时间的时间差，得到每次执行的时间间隔
    interval = (next_run_time_seconds - time.time()) / TIMES_A_DAY
    # 等待到下一次执行时间
    time.sleep(interval)
    print(f'将于{interval}秒后开始任务')
    #开始执行
    #检测游戏是否运行，如果没有运行就启动游戏
    adb.is_game_on()
    #path.to_menu()
    #换号(如不需要，请注释掉)
    path.to_login()
    time.sleep(1)
    adb.touch([917,584])
    time.sleep(0.5)
    adb.touch([801,336])
    time.sleep(0.5)
    adb.touch([667,394])
    time.sleep(1)
    adb.input('account')
    time.sleep(1)
    adb.touch([674,459])
    time.sleep(1)
    adb.input('password')
    time.sleep(1)
    out=f.cut_find_html('imgs/login_confirm',414,402,658,585,False)
    if out is None:
        adb.touch([612,557])#同意协议
        time.sleep(1)
    adb.touch([801,629])
    time.sleep(1)
    #换号结束
    path.to_menu()
    active.to_resource()
    #看看能不能直接进入意志解析，能就直接打，不能就去打本
    res=f.find(active.IMAGE_ANALYSIS)
    if res[2] >0.6:
        print('白嫖解析')
        active.Auto_Active(active.IMAGE_ANALYSIS, 7, active.REPLAY_2,False,1)
    path.to_menu()
    active.Auto_Active(active.IMAGE_HARVEST, 4, active.REPLAY_4,True,1)
    path.to_menu()
    #active.Auto_Active(active.IMAGE_HARVEST, 4, active.REPLAY_1,True,1)
    wilderness.wild_start()
    mission.mission_start()
    autopass.pass_start()
    #账号二（复制粘贴一下就行）





