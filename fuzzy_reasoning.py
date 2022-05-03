# %%
import pandas as pd
import numpy as np
from fuzzy_model import get_fuzzy_value

'''急迫性權重'''
def get_weight(low,high):
    return low, 1 - low - high, high

'''提取:1 不動作:0 解繳-1'''
def get_action(action):
    if action ==0 :
        a =0
    elif action >0:
        a =1
    else:
        a = -1

    return a

'''計算決策分數 插單解繳rush_order=-1 插單提取rush_order=1'''
def decision_score(fuzzy_level, action, rush_order=0, f_low=1/3, f_high=1/3):
    f_low, f_med, f_high = get_weight(f_low,f_high)
    score = fuzzy_level[1]*f_low + fuzzy_level[2]*f_med + fuzzy_level[3]*f_high
    action = get_action(action)
    decision_score = action * score
    decision_score += rush_order

    return decision_score

'''模糊推理引擎 產出各分行運補優先分數'''
# 後續看緊急插單需求是怎麼提供的，會再補上緊急插單的部分
def fuzzy_reasoning(action_list, rush_order_list):
    banklist = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 101, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 115, 116, 117, 118, 119, 120, 121, 122, 123, 125, 126,
            127, 128, 129, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 143, 144, 145, 146, 147, 148, 149, 150, 153, 154, 155, 156, 157, 158, 159, 160, 162, 164, 165, 166, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 185, 186, 187, 188, 189, 190, 192, 193, 196]
    ds = np.zeros((197,2))
    # 讀取fuzzy值
    fuzzy_value = get_fuzzy_value()
    for banknum in banklist:
        # 判斷是否有緊急插單需求
        if rush_order_list[banknum] & (action_list[banknum]>0):
            rush_order = 1
        elif rush_order_list[banknum] & (action_list[banknum]<0):
            rush_order = -1
        else:
            rush_order = 0
        d = decision_score(
            fuzzy_value[banknum],
            action_list[banknum],
            rush_order
        )
        ds[banknum] = [(banknum),d]

    return ds #pd.DataFrame(ds)

'''提取和解繳分行數量為 n_bank'''
# 目前需求為回傳急迫度即可，這個不會使用到
def get_action_bank(decision_score,n_bank):
    decision_score = decision_score[decision_score[1]!=0]
    decision_score = decision_score.sort_values([1])
    p_bank = list(decision_score.iloc[:n_bank,0])
    u_bank = list(decision_score.iloc[-n_bank:,0])
    all_bank = []
    all_bank.append([u_bank,p_bank])
    all_bank = np.array(all_bank).flatten()
    all_bank.sort()
    return all_bank, p_bank, u_bank

if __name__=="__main__":
    # 隨機產生動作進行測試
    action_list= np.random.random_integers(-3000000,3000000,size=(197,))
    # 隨機產生緊急插單需求進行測試
    rush_order_list = np.random.choice([True,False],size=(197,))
    # run
    decision_value = fuzzy_reasoning(action_list, rush_order_list)

# %%