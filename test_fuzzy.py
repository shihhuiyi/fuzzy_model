# %%
from fuzzy_model import get_fuzzy_value
from fuzzy_reasoning import fuzzy_reasoning
import pandas as pd

df = pd.read_csv("all3.csv",index_col=0)
df = df[df["date"].astype(str)=="20210527"]
df["action"] = df["take_money"] - df["deposit_money"]
# %%
import numpy as np
fuzzy_value = get_fuzzy_value()
action_list = np.zeros(197)
for banknum, action in zip(df.banknum, df.action):
        action_list[banknum] = action
decision_value = fuzzy_reasoning(action_list, np.array([False]*197))
# %%
df_dec = pd.DataFrame(decision_value)
df_dec = df_dec[df_dec[0]!=0]


# %%
import matplotlib.pyplot as plt
plt.figure(figsize=(20,5))
plt.bar(np.arange(125),df_dec[1],label = "decision value")
plt.xticks(range(125),df_dec[0].astype(int),rotation =90,fontsize=8)
plt.grid()
plt.legend()
plt.xlim(-1,126)
# %%
from fastapi import FastAPI
from fuzzy_model import get_fuzzy_value
from fuzzy_reasoning import fuzzy_reasoning

app = FastAPI()

@app.get("/fuzzy/fuzzy_value")
async def get_fuzzy_value_by_banknum(banknum:int):
        fuzzy_value = get_fuzzy_value()
        return {"fuzzy_value":str(fuzzy_value[banknum][0])}

# %%
fuzzy_value = get_fuzzy_value()
# %%
