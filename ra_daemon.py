import sys
import os
import time
import subprocess
import traceback
from datetime import datetime
import multiprocessing
import psutil
import itertools

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
                case 'user':
                    config.set_user(value)
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
        time.sleep(20)
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
    os.system('taskkill /im MuMuPlayer.exe')
    time.sleep(5)
    return
    if emulator_pid == -1:
        logger.warning("pid=-1, 模拟器未启动")
        return True
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

def work_favor():
    logger.info("开始信任互动")
    for _ in range(3):
        adb.touch((800, 450))
        time.sleep(0.3)
    time.sleep(3)
    return True

def work_fusing():
    return mission.get_fusing_box()

def work_fight(fight: dict, energy: int):
    assert path.to_menu()
    as_much=False
    if fight['asmuch']:
        as_much=True
    if fight['times'] == 0:
        return '设置为 0 次，跳过'
    if fight['hard'] > 3:
        raise Exception("难度设置超出范围")
    match list(fight['name']):
        case '主', '线', x:
            x = int(x)
            entry = active.IMAGE_CHAPTERX % x
            times = None if fight['asmuch'] else fight['times']
            if times is None:
                as_much = True
            active.enter_the_show()
            assert fight['hard'] > 0, f'主线难度不应设置为童话'
            hard_handle = lambda: active.choose_story_hardness(fight['hard'])
            return active.Auto_Active(
                entry,
                fight['level'],
                times,
                False, 1,
                hard_handle,
                as_much, energy
            )
        case '意', *_: # 意志解析
            active.to_resource()
            if f.find(active.IMAGE_ANALYSIS)[2] > 0.6: # 仅免费解析
                logger.info('进行免费解析')
                return active.Auto_Active(
                    active.IMAGE_ANALYSIS,
                    fight['level'], 2,
                    False, 1
                ) or '免费解析2次'
            return '无免费次数，跳过'
        case '尘', *_: # 尘埃运动
            return active.Auto_Active(
                active.IMAGE_THE_POUSSIERE,
                fight['level'],
                fight['times'],
                True, 1,
                None, as_much, energy
            )
        case '铸', *_: # 铸币美学
            return active.Auto_Active(
                active.IMAGE_MINTAGE_AESTHETICS,
                fight['level'],
                fight['times'],
                True, 1,
                None, as_much, energy
            )
        case '丰', *_: # 丰收时令
            return active.Auto_Active(
                active.IMAGE_HARVEST,
                fight['level'],
                fight['times'],
                True, 1,
                None, as_much, energy
            )
        case '群'|'星'|'深'|'荒', *_: # 洞悉
            entry = active.IMAGE_INSIGHT_MAP[fight['name']]
            active.to_insight()
            return active.Auto_Active(
                entry,
                fight['level'],
                fight['times'],
                False, 1,
                None, as_much, energy
            )
        case '活', *_: # 当期活动
            logger.info('打活动（当前 V1.6 朔日手记）')
            active.to_festival()
            time.sleep(2) # wait for animation
            hard_handle = lambda: active.choose_festival_hardness(fight['hard'])
            return active.Auto_Active(
                active.IMAGE_GOLDEN_MAINLINE,
                fight['level'],
                fight['times'],
                False, 6,
                hard_handle,
                as_much, energy
            )
        case name:
            logger.error(f"未知任务名 {name}")
            raise NotImplementedError

def work(task: dict, summary: list[str]):
    all_success = True
    # Favorability
    try:
        res = work_favor()
        summary.append("信任：互动完成")
        logger.success("信任：互动完成")
    except Exception as e:
        all_success = False
        summary.append(f"信任：互动失败: {e}")
        logger.error(traceback.format_exc())
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
    # Fusing Box
    try:
        if task['detail'].get('fusing', True):
            assert work_fusing()
            summary.append(f"定影匣子: 领取完成")
            logger.success('定影匣子: 领取完成')
    except Exception as e:
        all_success = False
        summary.append(f"定影匣子: 领取失败: {e}")
        logger.error(traceback.format_exc())

def loop(accounts):
    logger.success('进入任务循环')
    global game_login
    global game_password
    global game_account
    for username, password in itertools.cycle(accounts):
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
                    time.sleep(2.) # 等待成就动画

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
                        with open(log_path, 'r', encoding='utf-8') as f:
                            history_log = f.readlines()[-20:]
                            history_log = ''.join(history_log)
                        summary.append(f'发生未知错误: {repr(e)}, 执行中断')
                        client.log(token, task_id, client.LogLevel.ERROR, f'未知错误: {trace_info}')
                        client.notify(token, task_id, '发生未知错误', history_log)
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

def pre_check(username: str, password: str):
    if config.user_config.get('skipPreCheck', False):
        logger.info("跳过预检查")
        return
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
        
        if not startup_program():
            raise Exception('模拟器启动失败')
        if not adb.is_device_connected():
            raise Exception('连接设备失败')
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

@logger.catch
def main():
    config.check_path()
    # sys.argv = [sys.argv[0], 'admin', 'admin'] # debug
    if len(sys.argv) > 1:
        webui_accounts = sys.argv[1: 3]
    else:
        webui_accounts = config.user_config['webui_accounts']
    assert len(webui_accounts)
    
    if 'server' in config.user_config:
        client.set_server(config.user_config['server'])
    
    for user, pwd in webui_accounts:
        pre_check(user, pwd)
    
    loop(webui_accounts)

if __name__ == '__main__':
    main()