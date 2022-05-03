# %%
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from matplotlib import *



# Redefine the trimf function from skfuzzy. Let the linear function to become quadratic function. Initial power is 1.5.
def trimf_power(x, abc):
    assert len(abc) == 3, 'abc parameter must have exactly three elements.'
    a, b, c = np.r_[abc]     # Zero-indexing in Python
    assert a <= b and b <= c, 'abc requires the three elements a <= b <= c.'

    y = np.zeros(len(x))

    # Left side
    if a != b:
        idx = np.nonzero(np.logical_and(a < x, x < b))[0]
        y[idx] = np.square(((x[idx] - a) / float(b - a)))

    # Right side
    if b != c:
        idx = np.nonzero(np.logical_and(b < x, x < c))[0]
        y[idx] = np.square(((c - x[idx]) / float(c - b)))

    idx = np.nonzero(x == b)
    y[idx] = 1
    return y


# Redefine the trapmf function from skfuzzy. Let the linear function to become quadratic function. Initial power is 1.5.
def trapmf_power(x, abcd):
    assert len(abcd) == 4, 'abcd parameter must have exactly four elements.'
    a, b, c, d = np.r_[abcd]
    assert a <= b and b <= c and c <= d, 'abcd requires the four elements \
                                          a <= b <= c <= d.'
    y = np.ones(len(x))

    idx = np.nonzero(x <= b)[0]
    y[idx] = trimf_power(x[idx], np.r_[a, b, b])

    idx = np.nonzero(x >= c)[0]
    y[idx] = trimf_power(x[idx], np.r_[c, c, d])

    idx = np.nonzero(x < a)[0]
    y[idx] = np.zeros(len(idx))

    idx = np.nonzero(x > d)[0]
    y[idx] = np.zeros(len(idx))

    return y

def get_fuzzy_value():
    #分行代碼最大值（非分行總數之實際數量，因分行代碼為非連續，故array中存在空的元素）
    #目前分行代碼最大值為196，故array size =197
    branchAmount = int(197)

    #存取此時各分行的現金庫存水位
    #Bank_branches_cash_repository.csv 為測試資料
    bank_repository_now = np.zeros(shape=(branchAmount,1))
    # bank_repository_now = np.genfromtxt('Bank_branches_cash_repository.csv',delimiter=',',skip_header=1,usecols=(1))

    # 測試真實資料
    import pandas as pd
    df = pd.read_csv("all3.csv",index_col=0)
    df = df[df["date"].astype(str)=="20210527"]
    df.cash_t = df.cash_t/1000000
    for banknum, cash in zip(df.banknum, df.cash_t):
        bank_repository_now[banknum] = cash
    bank_repository_now = bank_repository_now.flatten()

    #此fuzzy sets 之X軸為 cash_repository ，即庫存限額，單位為百萬
    cashMin = 0
    cashMax = 80
    #即fuzzy sets中的x軸
    X_cash_repository = np.arange(cashMin,cashMax,0.1)


    #在平常（非峰日、非年節）情況下，將所有分行的fuzzy set存在bank_branch_normal中，預設array size =197，各分行對應至bank_branch_mormal[分行代碼]
    bank_branch_normal = np.ndarray(shape=(branchAmount,3,len(X_cash_repository)))
    ''' 目前只考慮一般情況
    #在峰日情況下，將所有分行的fuzzy set存在bank_branch_busy中，預設array size =197，各分行對應至bank_branch_busy[分行代碼]
    bank_branch_busy = np.ndarray(shape=(branchAmount,3,len(X_cash_repository)))
    #在年節情況下，將所有分行的fuzzy set存在bank_branch_busy中，預設array size =197，各分行對應至bank_branch_busy[分行代碼]
    bank_branch_NewYear = np.ndarray(shape=(branchAmount,3,len(X_cash_repository)))
    '''

    #讀取各分行fuzzy sets資料之csv檔
    fuzzy_sets = np.genfromtxt('Bank_branches_fuzzy_sets.csv',delimiter=',',skip_header = 1)

    #利用skfuzzy，製作各間分行的fuzzy sets
    for i in range(branchAmount):
        bank_branch_normal[i][0] = trapmf_power(X_cash_repository,[cashMin,cashMin,fuzzy_sets[i][4],fuzzy_sets[i][5]])
        bank_branch_normal[i][1] = fuzz.trimf(X_cash_repository,[fuzzy_sets[i][6],fuzzy_sets[i][7],fuzzy_sets[i][8]])
        bank_branch_normal[i][2] = trapmf_power(X_cash_repository,[fuzzy_sets[i][9],fuzzy_sets[i][10],cashMax,cashMax])

    '''
    # 畫出 bank 2 的fuzzy圖
    plt.plot(X_cash_repository,bank_branch_normal[196][0]) #過低
    plt.plot(X_cash_repository,bank_branch_normal[196][1]) #適中
    plt.plot(X_cash_repository,bank_branch_normal[196][2]) #過高
    '''

    #存取各分行對應的fuzzy value於cash_repository_level中，array shape = 197 x 4
    #col: 0:分行代碼 1:low 2:mid 3:high
    cash_repository_level = np.ndarray(shape = (branchAmount,4))
    #存取fuzzy values
    for i in range(branchAmount):
        cash_repository_level[i][0] = i
        cash_repository_level[i][1] = fuzz.interp_membership(X_cash_repository,bank_branch_normal[i][0],bank_repository_now[i])
        cash_repository_level[i][2] = fuzz.interp_membership(X_cash_repository,bank_branch_normal[i][1],bank_repository_now[i])
        cash_repository_level[i][3] = fuzz.interp_membership(X_cash_repository,bank_branch_normal[i][2],bank_repository_now[i])

    return cash_repository_level

if __name__ == "__main__":
    fuzzy_value = get_fuzzy_value()
    print(fuzzy_value[196]) #查詢196的fuzzy值
# %%
