from time import sleep
from abd_command import touch
from find import search_cards,calculate
from cards.aname import buff,debuff,attack,limit
from config.mappoint import clickcard
import api
import cv2 as cv
class Turn:
    buff:int = 0
    debuff:int = 0
    count:int = 0
    card:list = []
def next_card(t:Turn,i:int):
    while(True):
        i -= 1
        if (i == -1):
            break
        t.card[i+1] = t.card[i]
    t.card[0] = '无卡牌'

def Limit(t:Turn):
    for j in range(0,7):
        i = 6-j
        if t.card[i] in limit:
            print(t.card[i] )
            touch(clickcard[i][1],clickcard[i][0])
            next_card(t,i)
            print(t.card)
            sleep(1)
            return 1
    return 0

def useBuff(t:Turn):
    for j in range(0,7):
        i = 6-j
        if t.card[i] in buff:
            print(t.card[i] )
            touch(clickcard[i][1],clickcard[i][0])
            next_card(t,i)
            print(t.card)
            sleep(1)
            return 1
    return 0

def useDebuff(t:Turn):
    for j in range(0,7):
        i = 6-j
        if t.card[i] in debuff:
            print(t.card[i] )
            touch(clickcard[i][1],clickcard[i][0])
            next_card(t,i)
            print(t.card)
            sleep(1)
            return 1
    return 0

def Attack(t:Turn):
    for j in range(0,7):
        i = 6-j
        if t.card[i] in attack:
            print(t.card[i] )
            touch(clickcard[i][1],clickcard[i][0])
            next_card(t,i)
            print(t.card)
            sleep(1)
            return 1
    return 0

def startTurn(t:Turn):
    api.get_screen_shot()
    ans = search_cards()
    if (ans[6] == '无卡牌' and ans[3] == '无卡牌'):
        return
    print("回合开始")
    t.buff -=1
    t.debuff -=1
    use = 0
    t.card = search_cards()
    print(t.card)
    if (t.buff <= 0):
        use += useBuff(t)
        t.buff = 2
    if (t.debuff <= 0):
        use += useDebuff(t)
        t.debuff = 2
    for i in range(0,3):
        if use < 3:
            use += Limit(t)
    for i in range(0,3):
        if use < 3:
            use += Attack(t)
    
    

def checkTurn(t:Turn):
    while(True):
        api.get_screen_shot()
        # img  = cv.imread("screenshot.png")
        # x = 190
        # y = 778
        # img = img[x:118,y:85]
        # checker = cv.imread("cards/disappear.png")
        # if calculate(checker,img) > 0.6:
        ans = search_cards()
        if (ans[6] != '无卡牌' and ans[3] != '无卡牌'):
            print("start")
            sleep(1.5)
            startTurn(t)
        print("休息中",t.debuff,t.buff)
        sleep(0.2)
t = Turn()
checkTurn(t)
