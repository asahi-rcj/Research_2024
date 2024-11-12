# ナップサック問題
# 容量 N のナップサックに、(価値,容量)=(an, bn)と指定された荷物を入れていく
# N を超えない容量までナップサックに入れた時の価値の最大はいくらか？

# これを遺伝的アルゴリズムを使って解く。

import pprint
import random
import math
import os

# ナップサックに入る荷物の限界量
NAP_LIMIT = 500

# 各遺伝子が持つ「バッグに荷物を積めるかどうか」
#  = 荷物の数 
ITEM_COUNT = 10

# 各世代の個体
EACH_LEVEL_COUNT = 100

# 次世代生成数
GENERATION_TIME = 500

# 交配レート
CROSS_RATING = 95
MUTANT_RATING = 5

#value, weight
item = []

def init_each_param_from_text():
    dirname = os.path.dirname(__file__)
    f = open(os.path.join(dirname, "question.txt"), 'r', encoding='UTF-8')
    data_list = f.readlines()

    global ITEM_COUNT
    global NAP_LIMIT

    line_count = 0
    for i in data_list:
        if line_count == 0:
            ITEM_COUNT = int(i.split(' ')[0])
            NAP_LIMIT = int(i.split(' ')[1])
        else:
            item.append((int(i.split(' ')[0]), int(i.split(' ')[1])))

        line_count = line_count + 1

    # 各個体設定

def init_each_individual():
    for i in range(0, EACH_LEVEL_COUNT):
        for j in range(0, ITEM_COUNT):
            E[i][j] = math.floor(random.random()*2)


#init_each_param()
init_each_param_from_text()

E = [[0] * ITEM_COUNT for i in range(EACH_LEVEL_COUNT)]

def main():

    init_each_individual()

    for i in range(GENERATION_TIME):
        # 各個体の総重量・価値を計算する

        nap_amount = []
        nap_value = []
        for j in range(EACH_LEVEL_COUNT):
            nap_amount.append(judge_each_napsak_amount(E[j]))
            nap_value.append(judge_each_napsak_value(E[j]))
        
        if i == 0:
            print ("【" + str(i) + "世代目 現世代遺伝子】")
            for j in range(EACH_LEVEL_COUNT):
                print(str(E[j]) + ", 重量:" + str(judge_each_napsak_amount(E[j])) + ", 価値:" + str(judge_each_napsak_value(E[j])))


        #各個体の情報をもとにまずはエリート個体を2個選出する
        elite_value = sorted(nap_value, reverse=True)[:2]
        elite_index = [0, 0]
        elite_E = [[0] * ITEM_COUNT, [0] * ITEM_COUNT]


        for j in range(2):
            elite_index[j] = nap_value.index(elite_value[j])
            elite_E[j] = E[elite_index[j]]

        #次の世代の遺伝子配列を生成
        nextE = [[0] * ITEM_COUNT for i in range(EACH_LEVEL_COUNT)]


        #現在の世代の総価値を取得
        total_value = 0
        for j in range(EACH_LEVEL_COUNT):
            total_value += nap_value[j]

        #これらのデータをもとに次の世代に引き継ぐ遺伝子を取得する
        for j in range(EACH_LEVEL_COUNT):
            #まずは全価値を超えない範囲で基準価値を指定する
            select_base_value = math.floor(random.random() * total_value)
            select_sum_value = 0
            for k in range(EACH_LEVEL_COUNT):
                select_sum_value += nap_value[k]

                #もし基準価値を超えたら、それを次世代引継ぎ遺伝子として引き継ぐ
                if select_sum_value > select_base_value:

                    for l in range(ITEM_COUNT):
                        nextE[j][l] = E[k][l]
                    
                    #次の遺伝子取得に移る
                    break
        '''

        for j in range(EACH_LEVEL_COUNT):
            random_select = random.randint(0, EACH_LEVEL_COUNT - 1)
            for l in range(ITEM_COUNT):
                nextE[j][l] = E[random_select][l]
        '''

        # 次に、生成した次世代遺伝子を前から二つづつ取得し、交配させる
        # 交配方法：ある2点を取得し、その間の遺伝子を入れ替える

        for j in range(EACH_LEVEL_COUNT):

            # 現在交配基準遺伝子が奇数番目の場合、見送る
            if j % 2 == 1 or len(nextE) <= j + 1:
                continue

            # 交配するかどうかを選択
            crossrate = random.random() * 100

            # 事前に設定した交配率が達成されたら
            if crossrate < CROSS_RATING:
                cross_base_front = math.floor(random.randint(0, ITEM_COUNT))
                cross_base_back  = math.floor(random.randint(cross_base_front, ITEM_COUNT))

                for k in range(ITEM_COUNT):
                    if cross_base_front <= k and k <= cross_base_back:
                        _temp_data = nextE[j + 1][k]
                        nextE[j + 1][k] = nextE[j][k]
                        nextE[j][k] = _temp_data
            
            # 突然変異するかどうかを選択
            mutantrate = random.random() * 100

            # 事前に設定した突然変異率が達成されたら
            if mutantrate < MUTANT_RATING:
                select_m = math.floor(random.random() * ITEM_COUNT)
                nextE[j][select_m] = (nextE[j][select_m] + 1) % 2


        # 最後に、次世代遺伝子を現世代遺伝子に変更する
        for j in range(EACH_LEVEL_COUNT):
            for k in range(ITEM_COUNT):

                #最初の二つはエリート個体にする
                if j == 0 or j == 1:
                    E[j][k] = elite_E[j][k]
                else:
                    E[j][k] = nextE[j][k]


        if i == GENERATION_TIME - 1:
            print ("【" + str(i) + "世代目 次世代遺伝子】")

            for j in range(EACH_LEVEL_COUNT):
                print(str(judge_each_napsak_value(E[j])))
        else:
            print(i)


        
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
    
    amount = judge_each_napsak_amount(e)

    if amount > NAP_LIMIT:
        value = 0
    
    return value




if __name__ == "__main__":
    main()

