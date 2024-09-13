# ナップサック問題
# 容量 N のナップサックに、(価値,容量)=(an, bn)と指定された荷物を入れていく
# N を超えない容量までナップサックに入れた時の価値の最大はいくらか？

# これを遺伝的アルゴリズムを使って解く。

import random
import math

NAP_LIMIT = 1000

ITEM_COUNT = 10

EACH_LEVEL_COUNT = 10

#value, weight
item = []

E = [[0] * ITEM_COUNT for i in range(EACH_LEVEL_COUNT)]

def main():
    init_each_param()

def init_each_param():
    for i in range(0, ITEM_COUNT):
        item.append((random.randint(10, 100), random.randint(10, 100)))

    # 各個体設定

    for i in range(0, EACH_LEVEL_COUNT):
        for j in range(0, ITEM_COUNT):
            E[i][j] = math.floor(random.random()*2)

if __name__ == "__main__":
    main()

