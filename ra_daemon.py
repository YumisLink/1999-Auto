import sys
import os
import time
import subprocess
import traceback
from datetime import datetime
import multiprocessing
import psutil

from config import config

from lib import client
from lib import adb_command as adb
from lib import find as f

from lib.utils import save_img_log

from plugins import path
from plugins.san import get_san
from plugins import mail
from plugins import autopass
from plugins import wilderness
from plugins import mission
from plugins import active

from typing import Optional

from loguru import logger
log_path = os.path.join('logs', f'{datetime.now():%Y-%m-%d-%H-%M-%S}.log')
logger.add(log_path, level='DEBUG')

global emulator_pid
emulator_pid = -1
emulator_info={
    "mumu":{
        "exe_name":"MuMuPlayer.exe",
        "key":{"hide":"alt+q"},
        "random_port":False
    },
    "bs5":{
        "exe_name":"HD-Player.exe",
        "key":{"clear_memory":"ctrl+shift+t","hide":""},
        "random_port":False
    },
    "bs5hyper-v":{
        "exe_name":"HD-Player.exe",
        "key":{"clear_memory":"ctrl+shift+t","hide":""},
        "random_port":True
    },
}
global game_login
global game_password
global game_account
game_login=False

def log_callback(record: dict):
    if record['level'].name not in ['SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']:
        return record
    if config.user_config.get('image_log', False):
        save_img_log()
    return record
logger = logger.patch(log_callback)

def override_config(new_config: dict[str, str]):
    for key, value in new_config.items():
        try:
            logger.info(f"Override config: {key} => {value}")
            # ['emulator', 'adb_path', 'adb_port', 'device', 'channel', 'account', 'password']
            match key:
                case 'emulator':
                    raise NotImplementedError
                case 'adb_path':
                    raise NotImplementedError
                case 'adb_port':
                    raise NotImplementedError
                case 'device':
                    raise NotImplementedError
                case 'channel':
                    config.set_channel(value)
                case 'account':
                    global game_account
                    game_account=value
                case 'password':
                    global game_login
                    global game_password
                    game_login=True
                    game_password=value
                    logger.debug('账密登录开启')
                case _:
                    raise KeyError("Invalid override key")
        except Exception as e:
            logger.warning(f"Error: {e}")
            continue

def program_is_running() -> bool:
    p = subprocess.Popen('tasklist', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    emulator=config.user_config.get('emulator')
    try:
        return emulator_info[emulator]['exe_name'] in out.decode('gbk')
    except KeyError:
        logger.warning(f"unknown emulator:{emulator}")
        raise 

def hideMuMu():
    import pyautogui
    # pyautogui.press('Alt+Q')
    try:
        pyautogui.hotkey('alt', 'q')
    except Exception as e:
        logger.warning(f'Error: {e}')
    return

def start_emulator():
    emulator_arg = config.user_config.get('emulator_startarg')
    emulator_args = emulator_arg.split()
    # 启动模拟器并获取其 PID
    emulator_pid = -1
    try:
        proc = subprocess.Popen(emulator_args)
        time.sleep(30)
        adb_address = config.user_config.get('adb_address')
        adb_port = adb_address.split(':')[-1]
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN' and str(conn.laddr.port) == adb_port:
                emulator_pid = conn.pid
                break
    except OSError:
        emulator_pid = -1
        raise
    return emulator_pid

def startup_program():
    #if not config.user_config.get('Multi-emutalors', False):
    if program_is_running():
        logger.info('模拟器已经在运行')
        return True
    logger.info('正在启动模拟器')
    pid=start_emulator()
    if pid == -1:
        logger.error('模拟器启动失败')
        res=False        
    else:
        logger.success('模拟器启动成功')
        res=True
    if config.user_config.get('MuMuHeadless', False):
        hideMuMu()
    return res

def terminate_program():
    if config.user_config.get('emulator_KeepAlive', True):
        logger.info('保持模拟器运行不关闭')
        return
    logger.info('正在关闭模拟器')
    process = psutil.Process(emulator_pid)
    process.terminate()
    time.sleep(5)
    if program_is_running():
        logger.warning('模拟器关闭失败, 请手动关闭')
        return False
    logger.info('模拟器关闭成功')
    return True

def calc_energy(pre_time: datetime|str|float, pre_energy: int, now: Optional[datetime] = None) -> int:
    if isinstance(pre_time, str):
        pre_time = datetime.fromisoformat(pre_time)
    elif isinstance(pre_time, float):
        pre_time = datetime.fromtimestamp(pre_time)
    if now is None:
        now = datetime.now()
    dtime = now - pre_time
    energy_increase = dtime.total_seconds() / 360
    return int(pre_energy + energy_increase)

def work_mail():
    if not mail.mail_start():
        raise Exception('无法回到主界面')
    return

def work_wild():
    return wilderness.wild_start()

def work_pass():
    return autopass.pass_start()

def work_mission():
    return mission.mission_start()

def work_fight(fight: dict, energy: int):
    assert path.to_menu()
    as_much=False
    if fight['asmuch']:
        as_much=True
    match list(fight['name']):
        case '主', '线', x:
            x = int(x)
            entry = active.IMAGE_CHAPTERX % x
            times = None if fight['asmuch'] else fight['times']
            if times is None:
                as_much = True
            active.enter_the_show()
            if fight['hard'] > 1:
                hard_handle = active.choose_story_disaster
            else:
                hard_handle = lambda: active.IMAGE_START
            active.Auto_Active(
                entry,
                fight['level'],
                times,
                False, 1,
                hard_handle,
                as_much
            )
        case '意', *_: # 意志解析
            active.to_resource()
            if f.find(active.IMAGE_ANALYSIS)[2] > 0.6: # 仅免费解析
                logger.info('进行免费解析')
                active.Auto_Active(
                    active.IMAGE_ANALYSIS,
                    fight['level'], 2,
                    False, 1
                )
                return '免费解析2次'
            return '无免费次数，跳过'
        case '尘', *_: # 尘埃运动
            active.Auto_Active(
                active.IMAGE_THE_POUSSIERE,
                fight['level'],
                fight['times'],
                True, 1,
                None, as_much
            )
        case '铸', *_: # 铸币美学
            active.Auto_Active(
                active.IMAGE_MINTAGE_AESTHETICS,
                fight['level'],
                fight['times'],
                True, 1,
                None, as_much
            )
        case '丰', *_: # 丰收时令
            active.Auto_Active(
                active.IMAGE_HARVEST,
                fight['level'],
                fight['times'],
                True, 1,
                None, as_much
            )
        case '群'|'星'|'深'|'荒', *_: # 洞悉
            entry = active.IMAGE_INSIGHT_MAP[fight['name']]
            active.to_insight()
            active.Auto_Active(
                entry,
                fight['level'],
                fight['times'],
                False, 1,
                None, as_much
            )
        case '绿', *_: # 绿湖噩梦
            logger.info('打绿湖噩梦')
            active.to_festival()
            time.sleep(2) # wait for animation
            hard_handle = lambda: active.choose_green_lake(fight['hard'])
            active.Auto_Active(
                active.IMAGE_GREEN_MAINLINE,
                fight['level'],
                fight['times'],
                False, 1,
                hard_handle,
                as_much
            )

def work(task: dict, summary: list[str]):
    all_success = True
    # Mail
    try:
        if task['detail'].get('mail', False):
            work_mail()
            summary.append(f"邮件: 领取完成")
            logger.success('邮件: 领取完成')
    except Exception as e:
        all_success = False
        summary.append(f"邮件: 领取失败: {e}")
        logger.error(traceback.format_exc())
    # Wild
    try:
        if task['detail'].get('wild', False):
            res = work_wild()
            if res:
                summary.append(f"荒原: 领取完成")
                logger.success('荒原: 领取完成')
            else:
                summary.append(f"荒原: 无法回到主界面")
                logger.error('荒原: 无法回到主界面')
                adb.kill_app()
                assert adb.is_game_on()
    except Exception as e:
        all_success = False
        summary.append(f"荒原: 领取失败: {e}")
        logger.error(traceback.format_exc())
    # Fights
    for fight in task['detail'].get('fights', []):
        try:
            fight_name = f"{fight['name']}-{fight['level']}-难度{fight['hard']}"
            assert path.to_menu()
            energy = get_san()
            if not isinstance(energy, int):
                raise Exception('无法获取体力')
            msg = work_fight(fight, energy)
            summary.append(f"战斗: {fight_name} 执行完成{ f': {msg}' if msg else '' }")
            logger.success(f"战斗: {fight_name} 执行完成{ f': {msg}' if msg else '' }")
        except Exception as e:
            all_success = False
            summary.append(f"战斗: {fight['name']} 执行失败: {e}")
            logger.error(traceback.format_exc())
    # Pass
    try:
        if task['detail'].get('pas', False):
            work_pass()
            summary.append(f"点唱机: 领取完成")
            logger.success('点唱机: 领取完成')
    except Exception as e:
        all_success = False
        summary.append(f"点唱机: 领取失败: {e}")
        logger.error(traceback.format_exc())
    # Mission
    try:
        if task['detail'].get('mission', False):
            work_mission()
            summary.append(f"任务: 领取完成")
            logger.success('任务: 领取完成')
    except Exception as e:
        all_success = False
        summary.append(f"任务: 领取失败: {e}")
        logger.error(traceback.format_exc())
    return all_success

def loop(username: str, password: str):
    logger.success('进入任务循环')
    global game_login
    global game_password
    global game_account
    while True:
        game_login=False
        try:
            token = client.login(username, password)
            for task_id, task_name in client.get_tasks(token):
                logger.info(f"任务编号 {task_id}: {task_name}")
                summary = []
                skip = False
                start_time = datetime.now()
                try:
                    task = client.get_task(token, task_id)
                    if task['paused']:
                        logger.success(f"任务 {task_name} 被设为暂停，跳过")
                        skip = True
                        continue
                    client.log(token, task_id, client.LogLevel.HERTBEAT, '')
                    energy = calc_energy(task['time_stamp'], task['energy'])
                    if energy < 100: # TODO: get energy thresh from server
                        logger.success(f"任务 {task_name} 体力为{energy}, 未到执行阈值，跳过")
                        skip = True
                        continue
                    override_config(task['detail'].get('config_override', {}))
                    
                    if not startup_program():
                        raise Exception('模拟器启动失败')
                    if not adb.is_device_connected():
                        raise Exception('连接设备失败')
                    
                    if not adb.is_game_on():
                        raise Exception('游戏无法启动')
                    #login
                    if game_login:
                        logger.debug('开始进行账密登录')
                        path.login(game_account,game_password)
                        game_login=False
                    assert path.to_menu()

                    work(task, summary)
                    
                    assert path.to_menu()
                    energy = get_san()
                    if not isinstance(energy, int):
                        raise Exception('无法获取体力')
                    time_cost = datetime.now() - start_time
                    summary.append(f"任务 {task_name} 执行完成，剩余体力: {energy}, 耗时: {time_cost.total_seconds():.2f} 秒")
                    client.set_energy(token, task_id, energy)
                except Exception as e:
                    logger.error(f'=============== Uncaught Error in task {task_name}: {e} ===============')
                    try:
                        trace_info = traceback.format_exc()
                        logger.error(trace_info)
                        summary.append(f'发生未知错误: {e}, 执行中断')
                        client.log(token, task_id, client.LogLevel.ERROR, f'未知错误: {trace_info}')
                        client.notify(token, task_id, '发生未知错误', trace_info)
                    except Exception as e:
                        logger.error(f'=============== Uncaught Error in error handler: {e} ===============')                    
                finally:
                    if not skip:
                        summary = '\n'.join(summary)
                        logger.success("执行完成, 总结:\n" + summary)
                        try:
                            adb.kill_app()
                            client.log(token, task_id, client.LogLevel.NOTICE, summary)
                            client.notify(token, task_id, f'任务{task_name} 执行完成', summary)
                        except Exception as e:
                            logger.error(f'=============== Uncaught Error in summary: {e} ===============')
                
        except Exception as e:
            logger.error(f'=============== Uncaught Error: {e} ===============')
        finally:
            terminate_program()
            logger.info('等待 30 分钟')
            time.sleep(30 * 60) # 0.5 hours

@logger.catch
def main():
    config.check_path()
    if not startup_program():
        exit(1)
    device = adb.is_device_connected()
    if not device:
        logger.critical("Error: 未连接设备，请回看上面的错误信息")
        exit(1)
    # sys.argv = [sys.argv[0], 'admin', 'admin'] # debug
    username = sys.argv[1]
    password = sys.argv[2]
    if 'server' in config.user_config:
        client.set_server(config.user_config['server'])
    
    # Fetch tasks and update energy first
    # And we will basically check we are doing well, otherwise panic and exit
    token = client.login(username, password)
    need_terminate = True
    for task_id, task_name in client.get_tasks(token):
        global game_login
        global game_password
        global game_account
        game_login=False

        logger.info(f"预检查 任务编号 {task_id}: {task_name}")
        task = client.get_task(token, task_id)
        logger.debug(task)
        client.log(token, task_id, client.LogLevel.HERTBEAT, '')
        if task['paused']:
            logger.success(f"任务 {task_name} 被设为暂停，跳过")
            continue
        override_config(task['detail'].get('config_override', {}))
        if not adb.is_game_on():
            logger.critical('Error: 游戏无法启动')
            exit(1)
        if game_login:
            logger.debug('开始进行账密登录')
            path.login(game_account,game_password)
            game_login=False
        assert path.to_menu()
        energy = get_san()
        if energy is None:
            logger.critical('Error: 无法获取体力')
            exit(1)
        
        client.set_energy(token, task_id, energy)
        if energy > 100: # TODO: get energy thresh from server
            need_terminate = False
        adb.kill_app()
        logger.success(f"任务 {task_name} 预检查完成, 体力: {energy}")
    if need_terminate:
        terminate_program()
    
    loop(username, password)

if __name__ == '__main__':
    main()