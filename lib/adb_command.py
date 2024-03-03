import os
import json
import time
import re
from loguru import logger
from config.mappoint import clickcard
import config.config as config
import lib.api as api


def touch(point):
    'return zero if success else non-zero'
    if point[0] is None or point[1] is None:
        logger.warning(f"Invalid touching target")
        return -1
    logger.debug(f'click {point[0]} {point[1]}')
    return os.system(f'{config.ADB_HEAD} shell input tap {point[0]} {point[1]}')


def swipe(p1, p2, duration: int = None):
    duration = 300 if not duration else duration
    logger.debug(f'swipe from {p1[0]} {p1[1]} to {p2[0]} {p2[1]} in {duration}ms')
    os.system(f'{config.ADB_HEAD} shell input touchscreen swipe {p1[0]} {p1[1]} {p2[0]} {p2[1]} {duration}')
    
def input(text,clear=False):
    #print(f'input {text}')
    if clear:
        # 模拟按下“移动到行末”键
        os.system(f'{config.ADB_HEAD} shell input keyevent KEYCODE_MOVE_END ')
        # 模拟长按“删除”键250次
        os.system(f"{config.ADB_HEAD} input keyevent --longpress $(printf 'KEYCODE_DEL %.0s' {{1..250}})")
    logger.debug(os.system(f'{config.ADB_HEAD} shell input text {text}'))

def kill_app():
    logger.info(f'关闭 {config.APPID}')
    res = os.system(f'{config.ADB_HEAD} shell am force-stop {config.APPID}')
    logger.debug(f'关闭 {config.APPID} 结果：{res}')

def is_game_on(re_try=True):
    '''检测游戏是否在前台'''
    user_config = config.user_config
    adb_path = user_config['adb_path'] 
    command = (f'{config.ADB_HEAD} shell dumpsys window windows')
    try:
        process = os.popen(command)
        output = process.read()
        process.close()
        if config.APPID not in output:
            if not re_try:
                logger.info('游戏不在前台')
                return False
            # 应用不在前台，运行应用
            logger.info("游戏不在前台，正在启动")
            user = config.EXEC_USER
            if user:
                cmd = f'{config.ADB_HEAD} shell am start-user {user}'
                logger.debug(cmd)
                os.system(cmd)
                time.sleep(3)
            cmd = f'{config.ADB_HEAD} shell am start {f"--user {user}" if user else ""} {config.APPID}/{config.ACTIVITY}'
            logger.debug(cmd)
            # os.popen(f'{config.ADB_HEAD} shell monkey -p {config.APPID} -c android.intent.category.LAUNCHER 1')
            os.popen(cmd)
            time.sleep(8)
            return is_game_on(False)
        else:
            # 处理输出
            logger.debug('应用已在前台')
            return True
    except Exception as e:
        logger.error(f'Error: {e}')
        return False

def get_bluestacks_adb_port():
    # 读取bluestacks.conf文件
    bluestacks_adb_port_keys = config.user_config.get('bluestacks_adb_port_keys', [])
    bluestacks_conf_path = config.user_config.get('bluestacks_conf_path').strip()
    with open(bluestacks_conf_path, encoding="UTF-8") as f:
        configs = dict(list(map(lambda line: line.replace('\n', '').split('='), f.readlines())))
        return int(configs[bluestacks_adb_port_keys].replace('"', ""))


def check_device_connection():
    cfg = config.user_config
    adb_path = cfg['adb_path']
    device = None  # 初始化device变量为None
    if 'adb_address' in cfg and cfg['adb_address']:
        device = cfg['adb_address']
        os.system(f'{adb_path} connect {device}')
        # 通过验证adb devices命令的输出结果中List of devices attached下面是否有设备状态为device判断是否有设备连接
        output = os.popen(f'{adb_path} devices').read().strip().split('\n')
        if len(output) <= 1 or output[0] != 'List of devices attached':
            logger.error('Error: 无法连接adb_address，尝试连接蓝叠')
            blurestack=connect_bluestack()
            if blurestack:
                return blurestack
        else:
            logger.debug(f'已连接设备：{device}')
            config.user_config['device_id'] = device
            api.write_config()
            return device
    else:
        logger.error('Error:adb_address为空，尝试连接蓝叠')
        blurestack=connect_bluestack()
        if blurestack:
            return blurestack

def connect_bluestack():
    adb_path = config.user_config['adb_path']
    device = '127.0.0.1:' + str(get_bluestacks_adb_port())
    os.system(f'{adb_path} connect {device}')
    output = os.popen(f'{adb_path} devices').read().strip().split('\n')
    if len(output) <= 1 or output[0] != 'List of devices attached':
        logger.error('Error: 无法连接蓝叠(列表为空))')
        return None
    else:
        config.user_config['adb_address'] = device
        logger.debug(f'已连接设备：{device}')
        config.user_config['device_id'] = device
        api.write_config()
        logger.debug('已设置devide为蓝叠端口')
        return device
            
def is_device_connected():
    config.ADB_HEAD = ''
    device=None
    # 检查adb路径是否存在
    if 'adb_path' in config.user_config and os.path.exists(config.user_config['adb_path'].strip()):
        adb_path = config.user_config['adb_path']
    else:
        project_path = os.path.abspath(os.path.dirname(__file__))
        adb_path = os.path.join(project_path, 'adb\\adb.exe')
        config.user_config['adb_path']=adb_path
        api.write_config()
    # 检查adb是否存在
    result = os.system(f'{adb_path} version')
    if result != 0:
        logger.error('Error: config.json有关adb的设置有误')
    else:
        os.system(f'{adb_path} disconnect')
        os.system(f'{adb_path} kill-server')#TODO:没必要都kill-server
        device = check_device_connection()
        with open('config.json', 'r') as f:
            config.user_config = json.load(f)
        if 'device_id' in config.user_config and config.user_config['device_id'].strip():
            config.ADB_HEAD = f'{adb_path} -s {config.user_config["device_id"]}'
        else:
            config.ADB_HEAD = f'{adb_path}'
    logger.debug('已重组config.ADB_HEAD:',config.ADB_HEAD)  
    config.user_config['adb_head'] = config.ADB_HEAD#TODO:adb head的使用逻辑有问题，更新之后没法第一时间利用，就非得重启几次程序才能用
    api.write_config()
    return device
    
            