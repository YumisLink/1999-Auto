from plugins.Turn import Turn
import lib.api as api
from lib.adb_command import touch
from time import sleep
from lib.find import search_cards, calculate
from config.mappoint import clickcard
from decisions.decision_1 import normal_cards_upgrade





def startTurn(t: Turn):
    api.get_screen_shot()
    t.card = search_cards(t.team)
    if (t.card[6][0] == '无卡牌' and t.card[1][0] == '无卡牌'):
        return
    print("回合开始")
    t.debuff -= 1
    t.buff -= 1
    t.heal -= 1
    buffer = normal_cards_upgrade(t)
    print(buffer[0])
    touch(clickcard[buffer[0][0]])
    sleep(buffer[0][1])
    # print(buffer[1])
    touch(clickcard[buffer[1][0]])
    sleep(buffer[1][1])
    # print(buffer[2])
    touch(clickcard[buffer[2][0]])
    sleep(1.5)
    



def checkTurn(t: Turn):
    while(True):
        api.get_screen_shot()
        ans = search_cards(t.team)
        if (ans[6][0] != '无卡牌' and ans[1][0] != '无卡牌'):
            sleep(1.5)
            startTurn(t)
        print("休息中", t.debuff, t.buff)
        sleep(0.2)