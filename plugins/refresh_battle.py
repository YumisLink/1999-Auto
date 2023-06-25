import time

from wandb import alert
from lib import find
from plugins import active
import lib.adb_command as adb
from plugins import Turn
from collections import Counter

TOP_MIDDLE = (800, 10)
BATTLE_INFO = active.IMAGE_BATTLE_INFO
BATTLE_INFO_RESTART = active.IMAGE_BATTLE_INFO_RESTART
CONFIRM = "imgs/confirm"
EMPTY_CARD = "imgs/empty_card"

INFINITE_LOOP_MAX_COUNT = 15

def get_point(expected_scene):
    return find.find_boolean(expected_scene)


def is_in_scene(expected_scene):
    return get_point(expected_scene)[2]


def click(point):
    adb.touch(point)


"""
TODO: 暴力枚举, 然后根据card确定角色(3人局首轮必定所有人都有卡)。性能影响如何? 目前传team使用比较麻烦
"""
def collect_ally_cards(team):
    t = Turn.Turn()
    t.team = team
    t.card = find.search_cards(t.team)
    return t.card


def restart_battle():
    battle_info_point = get_point(BATTLE_INFO)
    if not battle_info_point[2]:
        return False
    try_limited(lambda: click(battle_info_point), lambda: not is_in_scene(BATTLE_INFO))
    battle_info_restart_point = get_point(BATTLE_INFO_RESTART)
    if not battle_info_restart_point[2]:
        return False
    try_limited(lambda: click(battle_info_restart_point), lambda: not is_in_scene(BATTLE_INFO_RESTART))
    confirm_point = get_point(CONFIRM)
    try_limited(lambda: click(confirm_point), lambda: not is_in_scene(CONFIRM))


def start(team, expected_ally_cards, expected_enemy_cards):
    condition_match = False
    while (True):
        # 0.7阈值会导致空白卡片识别经常误判
        # try_limited(lambda : doThenSleep(lambda: click(TOP_MIDDLE), 0.5), lambda: find.find(EMPTY_CARD)[2]>0.9)
        try_limited(lambda: click(TOP_MIDDLE), lambda: find.find(EMPTY_CARD)[2] > 0.9)

        ally_cards = collect_ally_cards(team)

        ally_cards_map = Counter(ally_cards)

        cards_all_match = True
        for attr in expected_ally_cards.keys():
            value = expected_ally_cards.get(attr)
            if ally_cards_map.get(attr) is None or ally_cards_map.get(attr) < value:
                cards_all_match = False
                break
        if not cards_all_match:
            restart_battle()
            continue
        # TODO: 识别敌方状态
        # enemy_cards = collect_enemy_cards();
        # if not cards_any_match(expected_enemy_cards, enemy_cards):
        #     restart_battle()
        #     continue

        condition_match = True
        break

    if not condition_match:
        raise "Unexpected"


def try_limited(do_func, break_condition):
    while_cnt = INFINITE_LOOP_MAX_COUNT
    while (while_cnt > 0):
        do_func()
        if break_condition():
            break
        while_cnt -= 1
    if while_cnt <= 0:
        raise RuntimeError("Exceed max loop count")
