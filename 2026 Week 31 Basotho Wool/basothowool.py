import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

df = pd.read_csv("basotho_wool.csv")

bg = "#FFFFFF"
text = "#111111"
muted = "#666666"
grid = "#E4E4E4"
blue = "#2B4F7A"
orange = "#D97932"
gold = "#D9A12E"
green = "#4F7D63"

df = df[df["ref_year"].between(2010,2024)].copy()

top = df.groupby("reporter_desc")["primary_value"].sum().nlargest(4).index.tolist()
colors = dict(zip(top,[blue,orange,gold,green]))

monthly = df[df["reporter_desc"].isin(top)].groupby(["reporter_desc","ref_month"],as_index=False)["primary_value"].sum()
monthly["share"] = monthly["primary_value"] / monthly.groupby("reporter_desc")["primary_value"].transform("sum")
monthly = monthly.pivot(index="reporter_desc",columns="ref_month",values="share").reindex(top).fillna(0)

months = np.arange(1,13)
labels = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
x = np.linspace(1,12,600)

fig, ax = plt.subplots(figsize=(14,10),facecolor=bg)
ax.set_facecolor(bg)

for month in months:
    ax.axvline(month,color=grid,linewidth=.7,zorder=0)

for i,country in enumerate(top[::-1]):
    values = monthly.loc[country].values
    smooth = gaussian_filter1d(values,1.05,mode="wrap")
    circular_x = np.arange(0,14)
    circular_y = np.r_[smooth[-1],smooth,smooth[0]]
    y = np.interp(x,circular_x,circular_y)
    y = y / y.max() * .78
    base = i * 1.15
    peak = int(np.argmax(smooth) + 1)

    ax.fill_between(x,base,base+y,color=colors[country],alpha=.68,zorder=2)
    ax.plot(x,base+y,color=colors[country],linewidth=2,zorder=3)
    ax.hlines(base,1,12,color=grid,linewidth=1,zorder=1)
    ax.text(.78,base+.08,country.upper(),ha="right",va="bottom",fontsize=13,fontweight="bold",color=colors[country])
    ax.text(12.18,base+.08,f"PEAK: {labels[peak-1]}",ha="left",va="bottom",fontsize=9.5,fontweight="bold",color=colors[country])

ax.set_xlim(.65,13.05)
ax.set_ylim(-.12,4.35)
ax.set_xticks(months)
ax.set_xticklabels(labels,fontsize=10.5,color=muted)
ax.set_yticks([])
ax.tick_params(axis="x",length=0,pad=10)

for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(.075,.955,"BASOTHO WOOL MARKETS KEEP DIFFERENT CALENDARS.",fontsize=28,fontweight="bold",color=text)
fig.text(.075,.905,"THE FOUR LARGEST IMPORTERS CONCENTRATE THEIR RECORDED TRADE VALUE IN DIFFERENT MONTHS.",fontsize=14,fontweight="bold",color=text)
fig.text(.075,.865,"MONTHLY SHARE OF EACH IMPORTER'S TOTAL BASOTHO WOOL TRADE VALUE, 2010–2024",fontsize=13,fontweight="bold",color=blue)
fig.text(.075,.055,"Each market is scaled independently to emphasize timing rather than total value. Monthly values are combined across 2010–2024.",fontsize=9.5,color=muted)
fig.text(.075,.025,"Source: UN Comtrade Database via TidyTuesday  |  Rowan Olson · #TidyTuesday",fontsize=9.5,color=muted)

plt.subplots_adjust(left=.20,right=.91,top=.80,bottom=.12)
plt.savefig("basothowool.png",dpi=300,bbox_inches="tight",facecolor=bg)
plt.show()