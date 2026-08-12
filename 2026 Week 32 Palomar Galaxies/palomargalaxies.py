import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Rectangle

df = pd.read_csv("palomar_survey.csv")

bg = "#FFFFFF"
text = "#111111"
muted = "#666666"
blue = "#2B4F7A"
red = "#B83B45"
orange = "#D97A1A"
green = "#4CA64C"
purple = "#765A9A"
gray = "#999999"

colors = {"H II":blue,"Seyfert":red,"LINER":orange,"Transition":green}
morph_colors = {"Elliptical":purple,"Lenticular":"#557A95","Early Spiral":"#C77D38","Late Spiral":"#5A8A65"}

d = df[["hubble_type","activity_type"]].dropna().copy()
d["hubble"] = d["hubble_type"].str.upper().str.replace(" ","",regex=False)

d["morphology"] = np.select([
    d["hubble"].str.match(r"^(D?E)\d|^(D?E)$"),
    d["hubble"].str.contains(r"^S0|^SB0|^RS0",regex=True),
    d["hubble"].str.contains(r"^SA|^SAB|^SB.*A|^S\(.*\)A|^S.*AB",regex=True),
    d["hubble"].str.contains(r"BC|^SC|^SCD|^SD|^SM|^IM|^IB|^SB.*[C-M]",regex=True)
],["Elliptical","Lenticular","Early Spiral","Late Spiral"],default="Other")

d = d[d["morphology"] != "Other"].copy()
d = d[d["activity_type"].isin(colors)].copy()

morph_order = ["Elliptical","Lenticular","Early Spiral","Late Spiral"]
activity_order = ["LINER","Transition","Seyfert","H II"]

flows = pd.crosstab(d["morphology"],d["activity_type"]).reindex(index=morph_order,columns=activity_order,fill_value=0)

left_totals = flows.sum(axis=1)
right_totals = flows.sum(axis=0)
total = flows.values.sum()

left_gap = .04
right_gap = .04

left_heights = left_totals / total * (1 - left_gap * (len(morph_order)-1))
right_heights = right_totals / total * (1 - right_gap * (len(activity_order)-1))

left_bottom = {}
right_bottom = {}

y = 1
for morphology in morph_order:
    y -= left_heights[morphology]
    left_bottom[morphology] = y
    y -= left_gap

y = 1
for activity in activity_order:
    y -= right_heights[activity]
    right_bottom[activity] = y
    y -= right_gap

fig, ax = plt.subplots(figsize=(14,10),facecolor=bg)
ax.set_facecolor(bg)

left_running = {m:left_bottom[m] for m in morph_order}
right_running = {a:right_bottom[a] for a in activity_order}

for morphology in morph_order:
    for activity in activity_order:
        n = flows.loc[morphology,activity]
        if n == 0:
            continue

        h = n / total * (1 - left_gap * (len(morph_order)-1))
        y0a = left_running[morphology]
        y0b = y0a + h
        y1a = right_running[activity]
        y1b = y1a + h

        verts = [
            (.18,y0a),(.40,y0a),(.60,y1a),(.82,y1a),
            (.82,y1b),(.60,y1b),(.40,y0b),(.18,y0b),
            (.18,y0a)
        ]

        codes = [
            Path.MOVETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,
            Path.LINETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,
            Path.CLOSEPOLY
        ]

        ax.add_patch(PathPatch(Path(verts,codes),facecolor=colors[activity],edgecolor="none",alpha=.28,zorder=1))
        left_running[morphology] += h
        right_running[activity] += h

for morphology in morph_order:
    y0 = left_bottom[morphology]
    h = left_heights[morphology]
    ax.add_patch(Rectangle((.10,y0),.08,h,facecolor=morph_colors[morphology],edgecolor="none",zorder=3))
    ax.text(.085,y0+h/2,morphology.upper(),ha="right",va="center",fontsize=12,fontweight="bold",color=morph_colors[morphology])
    ax.text(.085,y0+h/2-.026,f'n={left_totals[morphology]}',ha="right",va="top",fontsize=9,color=muted)

for activity in activity_order:
    y0 = right_bottom[activity]
    h = right_heights[activity]
    ax.add_patch(Rectangle((.82,y0),.08,h,facecolor=colors[activity],edgecolor="none",zorder=3))
    ax.text(.915,y0+h/2,activity.upper(),ha="left",va="center",fontsize=12,fontweight="bold",color=colors[activity])
    ax.text(.915,y0+h/2-.026,f'n={right_totals[activity]}',ha="left",va="top",fontsize=9,color=muted)

ax.text(.14,1.04,"GALAXY MORPHOLOGY",ha="center",va="bottom",fontsize=11,fontweight="bold",color=blue)
ax.text(.86,1.04,"NUCLEAR ACTIVITY",ha="center",va="bottom",fontsize=11,fontweight="bold",color=blue)

ax.set_xlim(0,1)
ax.set_ylim(-.04,1.08)
ax.axis("off")

fig.text(.075,.955,"DIVINING NUCLEAR ACTIVITY FROM A CORE",fontsize=27,fontweight="bold",color=text)
fig.text(.075,.905,"LATE SPIRAL GALAXIES ARE DOMINATED BY STAR-FORMING CENTERS. EARLIER FORMS ARE NOT.",fontsize=14,fontweight="bold",color=text)
fig.text(.075,.865,"NUCLEAR ACTIVITY ACROSS BROAD HUBBLE MORPHOLOGIES IN THE PALOMAR SURVEY",fontsize=13,fontweight="bold",color=blue)
fig.text(.075,.025,"Source: Palomar Spectroscopic Survey via TidyTuesday  |  Rowan Olson · #TidyTuesday",fontsize=9.5,color=muted)

plt.subplots_adjust(left=.08,right=.92,top=.80,bottom=.09)
plt.savefig("palomargalaxies.png",dpi=300,bbox_inches="tight",facecolor=bg)
plt.show()