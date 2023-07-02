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


def collect_ally(team):
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


def is_cards_match(expected_ally_cards, ally_cards_map):
    for card in expected_ally_cards.keys():
        expected_quantity = expected_ally_cards.get(card)
        if ally_cards_map.get(card) is None or ally_cards_map.get(card) < expected_quantity:
            return False
    return True


def start(team, expected_ally_list, expected_enemy_list):
    condition_match = False

    while (True):
        # 0.7阈值会导致空白卡片识别经常误判
        try_limited(lambda: click(TOP_MIDDLE), lambda: find.find(EMPTY_CARD)[2] > 0.9)

        ally = Counter(collect_ally(team))

        if any(is_cards_match(expected, ally) for expected in expected_ally_list):
            # TODO: 识别敌方状态
            condition_match = True
            break
        else:
            restart_battle()
            continue

    if not condition_match:
        raise "Unexpected"
    else:
        print("匹配到指定卡牌組合")

def try_limited(do_func, break_condition):
    while_cnt = INFINITE_LOOP_MAX_COUNT
    while (while_cnt > 0):
        do_func()
        if break_condition():
            break
        while_cnt -= 1
    if while_cnt <= 0:
        raise RuntimeError("Exceed max loop count")
