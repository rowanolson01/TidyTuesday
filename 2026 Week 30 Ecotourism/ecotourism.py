import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

df = pd.read_csv("occurrences.csv")

bg = "#FFFFFF"
text = "#111111"
muted = "#666666"
blue = "#2B4F7A"
pink = "#B54D78"
gold = "#D79B2A"
teal = "#36789B"
green = "#4F7D58"

world = gpd.read_file("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_0_countries.geojson")
aus = world.query("ADMIN == 'Australia'")

df = df[df["organism_name"].isin(["Orchid", "Gouldian finch", "Manta ray", "Glowworm"])].copy()
df["season"] = df["month"].map({12:"Summer",1:"Summer",2:"Summer",3:"Autumn",4:"Autumn",5:"Autumn",6:"Winter",7:"Winter",8:"Winter",9:"Spring",10:"Spring",11:"Spring"})

colors = {"Orchid":pink, "Gouldian finch":gold, "Manta ray":teal, "Glowworm":green}
seasons = ["Summer", "Autumn", "Winter", "Spring"]

fig, axes = plt.subplots(2, 2, figsize=(14, 11), facecolor=bg)
axes = axes.flatten()

for ax, season in zip(axes, seasons):
    d = df[df["season"] == season]
    aus.plot(ax=ax, facecolor="#F3F3F3", edgecolor="#C8C8C8", linewidth=.7)

    for organism, color in colors.items():
        group = d[d["organism_name"] == organism]
        ax.scatter(group["obs_lon"], group["obs_lat"], s=8 if organism == "Orchid" else 14, color=color, alpha=.22 if organism == "Orchid" else .52, edgecolors="none", 
            rasterized=True)

    ax.text(.02,.97,season.upper(),transform=ax.transAxes,ha="left",va="top",fontsize=15,fontweight="bold",color=blue)
    ax.set_xlim(112,154)
    ax.set_ylim(-44,-10)
    ax.set_aspect("equal")
    ax.axis("off")

fig.text(.075,.965,"FOUR SEASONS. FOUR WILDLIFE MAPS.",fontsize=29,fontweight="bold",color=text)
fig.text(.075,.920,"OBSERVATIONS SHIFT DRAMATICALLY THROUGHOUT THE AUSTRALIAN YEAR.",fontsize=14,fontweight="bold",color=text)
fig.text(.075,.882,"RECORDED OCCURRENCES OF FOUR FEATURED SPECIES, AUSTRALIA, 2014–2024",fontsize=13,fontweight="bold",color=blue)

legend_y = .842
legend_x = [.3, .43, .58, .7]

fig.text(legend_x[0],legend_y,"ORCHID",ha="center",fontsize=11.5,fontweight="bold",color=pink)
fig.text(legend_x[1],legend_y,"GOULDIAN FINCH",ha="center",fontsize=11.5,fontweight="bold",color=gold)
fig.text(legend_x[2],legend_y,"MANTA RAY",ha="center",fontsize=11.5,fontweight="bold",color=teal)
fig.text(legend_x[3],legend_y,"GLOWWORM",ha="center",fontsize=11.5,fontweight="bold",color=green)

fig.text(.075,.025,"Source: ecotourism package via TidyTuesday  |  Rowan Olson · #TidyTuesday",fontsize=9.5,color=muted)

plt.subplots_adjust(left=.04,right=.97,top=.80,bottom=.07,wspace=.02,hspace=.02)
plt.savefig("ecotourism.png",dpi=300,bbox_inches="tight",facecolor=bg)
plt.show()