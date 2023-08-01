import sys
import os
import time
import subprocess
import traceback
from datetime import datetime
import multiprocessing

from config import config

from lib import client
from lib import adb_command as adb
from lib import find as f

from plugins import path
from plugins.san import get_san
from plugins import mail
from plugins import autopass
from plugins import wilderness
from plugins import mission
from plugins import active

from typing import Optional

def program_is_running() -> bool:
    p = subprocess.Popen('tasklist', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return 'MuMuPlayer.exe' in out.decode('gbk')

def startup_program():
    if program_is_running():
        print('模拟器已经在运行')
        return True
    print('正在启动模拟器')
    os.system('start MuMu12.lnk')
    time.sleep(20)
    res = program_is_running()
    if res:
        print('模拟器启动成功')
    else:
        print('模拟器启动失败')
    return res

def terminate_program():
    os.system('taskkill /im MuMuPlayer.exe')
    time.sleep(5)
    if program_is_running():
        print('模拟器关闭失败, 强制关闭')
        os.system('taskkill /im MuMuPlayer.exe /f')
        time.sleep(5)
        if program_is_running():
            print('模拟器关闭失败, 请手动关闭')
            return False
    print('模拟器关闭成功')
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
    if fight['asmuch']:
        raise Exception('暂不支持“尽可能多”选项')
    match list(fight['name']):
        case '主', '线', x:
            x = int(x)
            entry = active.IMAGE_CHAPTERX % x
            times = None if fight['asmuch'] else fight['times']
            if times is None:
                raise Exception('暂不支持“尽可能多”选项')
            path.to_fight()
            active.Auto_Active(
                entry,
                fight['level'],
                times,
                False, 1
            )
        case '意', *_: # 意志解析
            active.to_resource()
            if f.find(active.IMAGE_ANALYSIS)[2] > 0.6: # 仅免费解析
                print('进行免费解析')
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
                True, 1
            )
        case '铸', *_: # 铸币美学
            active.Auto_Active(
                active.IMAGE_MINTAGE_AESTHETICS,
                fight['level'],
                fight['times'],
                True, 1
            )
        case '丰', *_: # 丰收时令
            active.Auto_Active(
                active.IMAGE_HARVEST,
                fight['level'],
                fight['times'],
                True, 1
            )
        case '群'|'星'|'深'|'荒', *_: # 洞悉
            entry = active.IMAGE_INSIGHT_MAP[fight['name']]
            active.Auto_Active(
                entry,
                fight['level'],
                fight['times'],
                True, 1
            )
        case '绿', *_: # 绿湖噩梦
            raise NotImplementedError('绿湖噩梦')
            # path.to_festival()

def work(task: dict, summary: list[str]):
    all_success = True
    # Mail
    try:
        if task['detail'].get('mail', False):
            work_mail()
            summary.append(f"邮件: 领取完成")
    except Exception as e:
        all_success = False
        summary.append(f"邮件: 领取失败: {e}")
    # Wild
    try:
        if task['detail'].get('wild', False):
            res = work_wild()
            if res:
                summary.append(f"荒原: 领取完成")
            else:
                print('荒原: 无法回到主界面')
                summary.append(f"荒原: 无法回到主界面")
                adb.kill_app()
                assert adb.is_game_on()
    except Exception as e:
        all_success = False
        summary.append(f"荒原: 领取失败: {e}")
    # Fights
    for fight in task['detail'].get('fights', []):
        try:
            assert path.to_menu()
            energy = get_san()
            if not isinstance(energy, int):
                raise Exception('无法获取体力')
            msg = work_fight(fight, energy)
            summary.append(f"战斗: {fight['name']} 执行完成{ f': {msg}' if msg else '' }")
        except Exception as e:
            all_success = False
            summary.append(f"战斗: {fight['name']} 执行失败: {e}")
    # Pass
    try:
        if task['detail'].get('pas', False):
            work_pass()
            summary.append(f"点唱机: 领取完成")
    except Exception as e:
        all_success = False
        summary.append(f"点唱机: 领取失败: {e}")
    # Mission
    try:
        if task['detail'].get('mission', False):
            work_mission()
            summary.append(f"任务: 领取完成")
    except Exception as e:
        all_success = False
        summary.append(f"任务: 领取失败: {e}")
    return all_success

def loop(username: str, password: str):
    while True:
        try:
            if not startup_program():
                raise Exception('模拟器启动失败')
            if not adb.is_device_connected():
                raise Exception('连接设备失败')
            token = client.login(username, password)
            for task_id, task_name in client.get_tasks(token):
                print(f"任务编号 {task_id}: {task_name}")
                client.log(token, task_id, client.LogLevel.HERTBEAT, '')
                summary = []
                skip = False
                try:
                    task = client.get_task(token, task_id)
                    if task['paused']:
                        print(f"任务 {task_name} 被设为暂停，跳过")
                        skip = True
                        continue
                    energy = calc_energy(task['time_stamp'], task['energy'])
                    if energy < 100: # TODO: get energy thresh from server
                        print(f"任务 {task_name} 体力未到执行阈值，跳过")
                        skip = True
                        continue
                    # TODO: get account info
                    if not adb.is_game_on():
                        raise Exception('游戏无法启动')
                    
                    work(task, summary)
                    
                    assert path.to_menu()
                    energy = get_san()
                    if not isinstance(energy, int):
                        raise Exception('无法获取体力')
                    summary.append(f"任务 {task_name} 执行完成，剩余体力: {energy}")
                    client.set_energy(token, task_id, energy)
                except Exception as e:
                    print(f'=============== Uncaught Error in task {task_name}: {e} ===============')
                    try:
                        trace_info = traceback.format_exc()
                        summary.append(f'发生未知错误: {e}, 执行中断')
                        client.log(token, task_id, client.LogLevel.ERROR, f'未知错误: {trace_info}')
                        client.email(token, task_id, '发生未知错误', trace_info)
                    except Exception as e:
                        raise
                finally:
                    if not skip:
                        client.log(token, task_id, client.LogLevel.NOTICE, '\n'.join(summary))
                
        except Exception as e:
            print(f'=============== Uncaught Error: {e} ===============')
        finally:
            terminate_program()
            print('等待 30 分钟')
            time.sleep(30 * 60) # 0.5 hours

if __name__ == '__main__':
    config.check_path()
    if not startup_program():
        exit(1)
    device = adb.is_device_connected()
    if not device:
        print("Error: 未连接设备，请回看上面的错误信息")
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
        print(f"任务编号 {task_id}: {task_name}")
        task = client.get_task(token, task_id)
        if task['paused']:
            print(f"任务 {task_name} 被设为暂停，跳过")
            continue
        # TODO: get account info
        if not adb.is_game_on():
            print('Error: 游戏无法启动')
            exit(1)
        assert path.to_menu()
        energy = get_san()
        if energy is None:
            print('Error: 无法获取体力')
            exit(1)
        
        client.set_energy(token, task_id, energy)
        if energy > 100: # TODO: get energy thresh from server
            need_terminate = False
    if need_terminate:
        terminate_program()
    
    print()
    loop(username, password)