import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

df = pd.read_csv("demo_by_reasons.csv")

bg = "#FFFFFF"
text = "#111111"
muted = "#666666"
grid = "#E3E3E3"
blue = "#2B4F7A"
orange = "#D97932"

d = df[(df["type"] == "Academic") & (df["year"] == "2024-2025")].copy()

band_map = {"<4":3.5,"4":4,"4.5":4.5,"5":5,"5.5":5.5,"6":6,"6.5":6.5,"7":7,"7.5":7.5,"8":8,"8.5":8.5,"9":9}
d["band_num"] = d["band"].map(band_map)

labels = {
    "For employment":"Employment",
    "For higher education extended course (three months or more)":"Extended higher education",
    "For higher education short course (three months or less)":"Short higher education",
    "For immigration":"Immigration",
    "For other education purposes":"Other education",
    "For personal reasons":"Personal reasons",
    "For professional registration (NOT medical)":"Professional registration",
    "For registration as a dentist":"Dentist registration",
    "For registration as a doctor":"Doctor registration",
    "For registration as a nurse (including CGFNS)":"Nurse registration",
    "(Other)":"Other"
}

d["reason_short"] = d["reason"].map(labels)

means = d.groupby("reason_short").apply(lambda x: np.average(x["band_num"],weights=x["percent"]),include_groups=False).sort_values()
order = means.index.tolist()

x = np.linspace(3.5,9,600)

fig, ax = plt.subplots(figsize=(14,11),facecolor=bg)
ax.set_facecolor(bg)

for i,reason in enumerate(order):
    r = d[d["reason_short"] == reason].sort_values("band_num")
    y = np.interp(x,r["band_num"],r["percent"])
    y = gaussian_filter1d(y,10)
    y = y / y.max() * .82
    base = i * 1.05

    ax.fill_between(x,base,base+y,color=blue,alpha=.22)
    ax.plot(x,base+y,color=blue,linewidth=1.8)
    ax.hlines(base,3.5,9,color=grid,linewidth=.8)

    mean = means[reason]
    ax.scatter(mean,base,s=54,color=orange,edgecolor="white",linewidth=1.2,zorder=4)
    ax.text(3.35,base+.07,reason.upper(),ha="right",va="bottom",fontsize=10.5,fontweight="bold",color=text)
    ax.text(9.15,base+.07,f"{mean:.2f}",ha="left",va="bottom",fontsize=10,fontweight="bold",color=orange)

ax.set_xlim(3.15,9.45)
ax.set_ylim(-.2,len(order)*1.05+.15)
ax.set_xticks(np.arange(4,9.5,.5))
ax.set_xticklabels([f"{v:g}" for v in np.arange(4,9.5,.5)],fontsize=10,color=muted)
ax.set_yticks([])
ax.tick_params(axis="x",length=0,pad=10)
ax.grid(axis="x",color=grid,linewidth=.7)
ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(.075,.955,"PURPOSE SEPARATES IELTS SCORE PROFILES.",fontsize=28,fontweight="bold",color=text)
fig.text(.075,.905,"SCORE DISTRIBUTIONS SHIFT SUBSTANTIALLY DEPENDING ON WHY PEOPLE TAKE THE EXAM.",fontsize=14,fontweight="bold",color=text)
fig.text(.075,.865,"ACADEMIC IELTS BAND DISTRIBUTIONS BY REASON FOR TESTING, 2024–2025",fontsize=13,fontweight="bold",color=blue)
fig.text(.075,.835,"ORANGE DOT = WEIGHTED AVERAGE BAND",fontsize=10.5,fontweight="bold",color=orange)
fig.text(.075,.025,"Source: IELTS via TidyTuesday  |  Rowan Olson · #TidyTuesday",fontsize=9.5,color=muted)

plt.subplots_adjust(left=.25,right=.90,top=.78,bottom=.09)
plt.savefig("ielts.png",dpi=300,bbox_inches="tight",facecolor=bg)
plt.show()