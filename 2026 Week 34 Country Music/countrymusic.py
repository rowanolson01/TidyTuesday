import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

df = pd.read_csv("country_lyrics.csv")

bg = "#FFFFFF"
text = "#111111"
muted = "#666666"
grid = "#E3E3E3"
blue = "#2B4F7A"
orange = "#D97932"

counts = df["artist"].value_counts()
artists = counts[counts >= 6].index.tolist()
collabs = {}

for artist in artists:
    d = df[df["artist"] == artist]
    people = set()

    for col in ["writers","producer"]:
        for value in d[col].dropna():
            for person in str(value).split(","):
                person = person.strip()
                if person and person.lower() != artist.lower():
                    people.add(person)

    collabs[artist] = people

worked_with = defaultdict(set)

for artist,people in collabs.items():
    for person in people:
        worked_with[person].add(artist)

rows = []

for artist,people in collabs.items():
    shared = {p for p in people if len(worked_with[p]) >= 2}
    unique = people - shared
    rows.append([artist,counts[artist],len(people),len(shared),len(unique),len(shared)/len(people)])

plot = pd.DataFrame(rows,columns=["artist","songs","collaborators","shared","unique","shared_share"])
plot["unique_share"] = 1 - plot["shared_share"]
plot = plot.sort_values("shared_share",ascending=True).reset_index(drop=True)

y = np.arange(len(plot))

fig, ax = plt.subplots(figsize=(13,11),facecolor=bg)
ax.set_facecolor(bg)

ax.barh(y,-plot["unique_share"]*100,height=.66,color=orange,alpha=.78)
ax.barh(y,plot["shared_share"]*100,height=.66,color=blue,alpha=.88)

for i,row in plot.iterrows():
    ax.text(-103,i,row["artist"].upper(),ha="right",va="center",fontsize=10.2,fontweight="bold",color=text)
    ax.text(103,i,f'{row["shared_share"]:.0%}',ha="left",va="center",fontsize=10,fontweight="bold",color=blue)

ax.axvline(0,color=text,linewidth=1.1)
ax.axvline(-50,color=grid,linewidth=.8)
ax.axvline(50,color=grid,linewidth=.8)

ax.text(-50,len(plot)+.15,"UNIQUE TO THIS ARTIST",ha="center",va="bottom",fontsize=11,fontweight="bold",color=orange)
ax.text(50,len(plot)+.15,"SHARED ACROSS NASHVILLE",ha="center",va="bottom",fontsize=11,fontweight="bold",color=blue)

ax.set_xlim(-108,112)
ax.set_ylim(-.75,len(plot)-.15)
ax.set_yticks([])
ax.set_xticks([-100,-75,-50,-25,0,25,50,75,100])
ax.set_xticklabels(["100%","75%","50%","25%","0","25%","50%","75%","100%"],fontsize=9.5,color=muted)
ax.tick_params(axis="x",length=0,pad=9)
ax.grid(False)

for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(.075,.955,"WHO SHARES NASHVILLE'S BACKSTAGE?",fontsize=27,fontweight="bold",color=text)
fig.text(.075,.905,"SOME COUNTRY STARS SHARE FAR MORE OF THEIR CREATIVE TEAMS THAN OTHERS.",fontsize=14,fontweight="bold",color=text)
fig.text(.075,.865,"WRITER & PRODUCER OVERLAP, 2013–2019",fontsize=13,fontweight="bold",color=blue)
fig.text(.075,.025,"Source: TidyTuesday  |  Rowan Olson · #TidyTuesday",fontsize=9.5,color=muted)

plt.subplots_adjust(left=.25,right=.91,top=.79,bottom=.09)
plt.savefig("countrymusic.png",dpi=300,bbox_inches="tight",facecolor=bg)
plt.show()