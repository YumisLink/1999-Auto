# 本方法在默认方法进行改进，有合卡的能力，但是决策同样是没buff续buff，没事干就续buff/debuff。
# 测试中
from Turn import Turn

def move(t:Turn,p:int):
    while(True):
        i -= 1
        if (i == -1):
            break
        t.card[i+1] = t.card[i]
        t.star[i+1] = t.star[i]
    t.card[0] = '无卡牌'
    t.star[0] = 0
    pass

# 与前一个合成
def upgrade(t:Turn,p:int):
    if is_same(t,p,p-1):
        move(t,p)
        t.star[p] += 1
    pass
def is_same(t:Turn,a:int,b:int):
    if t.card[a] == t.card[b] and t.star[a] == t.star[b]:
        return True
    return False

def normal_cards_upgrade(t:Turn):

    pass





