import os
import json
import time
import re
from config.mappoint import clickcard
from config.config import user_config,APPID,ADB_HEAD,DEVICE_ID
import lib.api as api


def touch(point):
    print(f'click {point[0]} {point[1]}')
    print(os.system(f'{ADB_HEAD} shell input tap {point[0]} {point[1]}'))


def swipe(p1, p2):
    print(f'swipe from  {p1[0]} {p1[1]} to {p2[0]} {p2[1]}')
    print(
        os.system(f'{ADB_HEAD} shell input touchscreen swipe {p1[0]} {p1[1]} {p2[0]} {p2[1]} 100'))
    
def input(text,clear=False):
    #print(f'input {text}')
    if clear:
        # 模拟按下“移动到行末”键
        os.system(f'{ADB_HEAD} shell input keyevent KEYCODE_MOVE_END ')
        # 模拟长按“删除”键250次
        os.system(f"{ADB_HEAD} input keyevent --longpress $(printf 'KEYCODE_DEL %.0s' {{1..250}})")
    print(os.system(f'{ADB_HEAD} shell input text {text}'))

def kill_app():
    print(f'关闭 {APPID}')
    print(os.system(f'{ADB_HEAD} shell am force-stop {APPID}'))
def is_game_on():
    '''检测游戏是否在前台'''
    config = user_config
    adb_path = config['adb_path'] 
    command = (f'{ADB_HEAD} shell dumpsys window windows')
    try:
        process = os.popen(command)
        output = process.read()
        process.close()
        if APPID not in output:
            # 应用不在前台，运行应用
            print("游戏不在前台，正在启动")
            os.popen(f'{ADB_HEAD} shell monkey -p {APPID} -c android.intent.category.LAUNCHER 1')
            time.sleep(8)
        else:
            # 处理输出
            print('应用已在前台')
    except Exception as e:
        print(f'Error: {e}')

def get_bluestacks_adb_port():
    # 读取bluestacks.conf文件
    bluestacks_adb_port_keys = user_config.get('bluestacks_adb_port_keys', [])
    bluestacks_conf_path = user_config.get('bluestacks_conf_path').strip()
    with open(bluestacks_conf_path, encoding="UTF-8") as f:
        configs = dict(list(map(lambda line: line.replace('\n', '').split('='), f.readlines())))
        return int(configs[bluestacks_adb_port_keys].replace('"', ""))
    # if not os.path.exists(bluestacks_conf_path):
    #     print(f'Error: 文件"{bluestacks_conf_path}"不存在')
    # else:
    #     with open(bluestacks_conf_path, 'r',encoding='utf-8') as f:
    #         conf = f.read()
    #     # 使用正则表达式匹配adb端口号
    #     for key in bluestacks_adb_port_keys:
    #         match = re.search(rf'{key}="(\d+)"', conf)
    #         if match:
    #             adb_port = match.group(1)
    #             return adb_port
    # return None

def check_device_connection():
    with open('config.json', 'r') as f:
        config = json.load(f)
    adb_path = config['adb_path']
    device = None  # 初始化device变量为None
    if 'adb_address' in config and config['adb_address']:
        device = config['adb_address']
        os.system(f'{adb_path} connect {device}')
        # 通过验证adb devices命令的输出结果中List of devices attached下面是否有设备状态为device判断是否有设备连接
        output = os.popen(f'{adb_path} devices').read().strip().split('\n')
        if len(output) <= 1 or output[0] != 'List of devices attached':
            print('Error: 无法连接adb_address，尝试连接蓝叠')
            blurestack=connect_bluestack()
            if blurestack:
                return blurestack
        else:
            print(f'已连接设备：{device}')
            config['device_id'] = device
            api.write_config()
            return device
    else:
        print('Error:adb_address为空，尝试连接蓝叠')
        blurestack=connect_bluestack()
        if blurestack:
            return blurestack

def connect_bluestack():
    adb_path = user_config['adb_path']
    device = '127.0.0.1:' + str(get_bluestacks_adb_port())
    os.system(f'{adb_path} connect {device}')
    output = os.popen(f'{adb_path} devices').read().strip().split('\n')
    if len(output) <= 1 or output[0] != 'List of devices attached':
        print('Error: 无法连接蓝叠(列表为空))')
        return None
    else:
        user_config['adb_address'] = device
        print(f'已连接设备：{device}')
        user_config['device_id'] = device
        api.write_config()
        print('已设置devide为蓝叠端口')
        return device
            
def is_device_connected():
    adb_head = ''
    device=None
    global user_config
    # 检查adb路径是否存在
    if 'adb_path' in user_config and os.path.exists(user_config['adb_path'].strip()):
        adb_path = user_config['adb_path']
    else:
        project_path = os.path.abspath(os.path.dirname(__file__))
        adb_path = os.path.join(project_path, 'adb\\adb.exe')
        user_config['adb_path']=adb_path
        api.write_config()
    # 检查adb是否存在
    result = os.system(f'{adb_path} version')
    if result != 0:
        print('Error: config.json有关adb的设置有误')
    else:
        device = check_device_connection()
        with open('config.json', 'r') as f:
            user_config = json.load(f)
        if 'device_id' in user_config and user_config['device_id'].strip():
            adb_head = f'{adb_path} -s {DEVICE_ID}'
        else:
            adb_head = f'{adb_path}'
    global ADB_HEAD
    print('已重组adb_head')
    ADB_HEAD = adb_head
    user_config['adb_head'] = adb_head#TODO:adb head的使用逻辑有问题，更新之后没法第一时间利用，就非得重启几次程序才能用
    with open('config.json', 'w') as f:
        json.dump(user_config, f, indent=4)
    return device
    
            