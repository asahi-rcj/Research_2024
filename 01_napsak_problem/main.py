# ナップサック問題
# 容量 N のナップサックに、(価値,容量)=(an, bn)と指定された荷物を入れていく
# N を超えない容量までナップサックに入れた時の価値の最大はいくらか？

# これを遺伝的アルゴリズムを使って解く。

import random
import math

NAP_LIMIT = 500

ITEM_COUNT = 10

EACH_LEVEL_COUNT = 10

GENERATION_TIME = 1

#value, weight
item = []

E = [[0] * ITEM_COUNT for i in range(EACH_LEVEL_COUNT)]

def main():
    init_each_param()

    for i in range(GENERATION_TIME):
        # 各個体の総重量・価値を計算する

        nap_amount = []
        nap_value = []
        for j in range(EACH_LEVEL_COUNT):
            nap_amount.append(judge_each_napsak_amount(E[j]))
            value = judge_each_napsak_value(E[j])

            if nap_amount[j] > NAP_LIMIT:
                nap_value.append(0)
            else:
                nap_value.append(value)

            print("総重量:" + str(nap_amount[j]) + ", 総価値:" + str(nap_value[j]))

        #各個体の情報をもとにまずはエリート個体を2個選出する
        elite_value = sorted(nap_value, reverse=True)[:2]
        elite_index = [0, 0]
        elite_E = [[0] * ITEM_COUNT, [0] * ITEM_COUNT]

        for j in range(2):
            elite_index[j] = nap_value.index(elite_value[j])

        print("エリート個体：" + str(elite_value))
        print("個体番号：" + str(elite_index))
        print("個体染色体：" + str(elite_E))


            

def judge_each_napsak_amount(e):
    amount = 0
    for i in range(ITEM_COUNT):
        if e[i] == 1:
            amount = amount + item[i][1]

    return amount


def judge_each_napsak_value(e):
    value = 0
    for i in range(ITEM_COUNT):
        if e[i] == 1:
            value = value + item[i][0]
    
    return value

def init_each_param():
    for i in range(0, ITEM_COUNT):
        item.append((random.randint(2, 10), random.randint(50, 100)))

    # 各個体設定

    for i in range(0, EACH_LEVEL_COUNT):
        for j in range(0, ITEM_COUNT):
            E[i][j] = math.floor(random.random()*2)

if __name__ == "__main__":
    main()

