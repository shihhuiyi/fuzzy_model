# %%
from turtle import color
import pandas as pd

df = pd.DataFrame()
df["route"] = ["R1","R2","R3","R4"]
df["rate"] =[0.5631,0.6796,0.6602,0.4563]
df = df.sort_values(["rate"])
# %%
import matplotlib.pyplot as plot

plot.bar(df["route"],df["rate"], width=0.4,label = "Concentrated rate")
plot.legend()
plot.ylim(0,1)
for a,b in zip(df["route"],df["rate"]):
    plot.text(a, b+0.05, '%.2f' % b, ha='center', va= 'bottom',fontsize=10)
# plot.scatter(df["route"],[df["rate"].mean()]*4,color = "red")
plot.savefig("/Users/shihuiyi/Desktop/rate.png")
# %%
