import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

df = pd.read_csv("many_penguins.csv")

bg = "#FFFFFF"
text = "#111111"
muted = "#666666"
grid = "#E3E3E3"
blue = "#264B73"

colors = {
    "Aptenodytes": "#2E5D87",
    "Eudyptes": "#D97732",
    "Eudyptula": "#5D8C60",
    "Megadyptes": "#B94747",
    "Pygoscelis": "#8A6FA8",
    "Spheniscus": "#8B6658"
}

traits = ["beak.length_culmen", "beak.length_nares", "beak.width", "beak.depth", "tarsus.length", "wing.length", "kipps.distance", "secondary1", "hand-wing.index", "tail.length"]

X = SimpleImputer(strategy="median").fit_transform(df[traits])
X = StandardScaler().fit_transform(X)

pca = PCA(n_components=2)
coords = pca.fit_transform(X)

plot = df[["species", "genus", "shortname"]].copy()
plot["PC1"] = coords[:, 0]
plot["PC2"] = coords[:, 1]

species = plot.groupby(["species", "genus", "shortname"], observed=True)[["PC1", "PC2"]].mean().reset_index()
centroids = plot.groupby("genus", observed=True)[["PC1", "PC2"]].mean().reset_index()

fig, ax = plt.subplots(figsize=(14, 10), facecolor=bg)
ax.set_facecolor(bg)

for genus, group in plot.groupby("genus", observed=True):
    color = colors[genus]
    points = group[["PC1", "PC2"]].to_numpy()
    center = points.mean(axis=0)
    cov = np.cov(points, rowvar=False)
    values, vectors = np.linalg.eigh(cov)
    order = values.argsort()[::-1]
    values = values[order]
    vectors = vectors[:, order]
    angle = np.degrees(np.arctan2(vectors[1, 0], vectors[0, 0]))
    width, height = 2 * 1.65 * np.sqrt(values)
    ax.add_patch(Ellipse(center, width, height, angle=angle, facecolor=color, edgecolor=color, linewidth=1.6, alpha=0.11, zorder=1))
    ax.scatter(group["PC1"], group["PC2"], s=34, color=color, alpha=0.27, edgecolor="none", zorder=2)

for genus, group in species.groupby("genus", observed=True):
    ax.scatter(group["PC1"], group["PC2"], s=120, color=colors[genus], edgecolor="white", linewidth=1.6, zorder=4)

label_offsets = {
    "Aptenodytes": (0.35, -0.15),
    "Eudyptes": (-0.8, 0.25),
    "Eudyptula": (-0.25, -0.10),
    "Megadyptes": (0.25, 0.18),
    "Pygoscelis": (0.25, -1),
    "Spheniscus": (0, 0.3)
}

for _, row in centroids.iterrows():
    dx, dy = label_offsets[row["genus"]]
    ax.text(row["PC1"] + dx, row["PC2"] + dy, row["genus"], ha="left" if dx >= 0 else "right", va="center", fontsize=13, fontweight="bold", color=colors[row["genus"]], zorder=5)

apt = centroids.loc[centroids["genus"] == "Aptenodytes"].iloc[0]

ax.annotate("The largest penguins occupy\ntheir own morphological space", xy=(5, 0), xytext=(3.25, 2.75), ha="left", va="center", fontsize=11.5, 
    fontweight="bold", color=blue, arrowprops=dict(arrowstyle="-", color=blue, linewidth=1.2))

ax.text(-1.9, 3.15, "Eudyptes and Pygoscelis share much of the same space", ha="center", va="center", fontsize=11, color=muted)

ax.axhline(0, color=grid, linewidth=1)
ax.axvline(0, color=grid, linewidth=1)
ax.grid(color=grid, linewidth=0.8)
ax.set_axisbelow(True)

ax.set_xlim(-4.35, 6.7)
ax.set_ylim(-3.45, 4.0)

ax.set_xlabel(f"PC1 · body size and overall scale ({pca.explained_variance_ratio_[0]:.1%})", fontsize=11, fontweight="bold", color=muted, labelpad=12)
ax.set_ylabel(f"PC2 · differences in body proportions ({pca.explained_variance_ratio_[1]:.1%})", fontsize=11, fontweight="bold", color=muted, labelpad=12)
ax.tick_params(axis="both", length=0, labelsize=10, colors=muted)

for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(0.075, 0.955, "MOST PENGUIN GENERA OCCUPY DISTINCT BODY PLANS.", fontsize=29, fontweight="bold", color=text)
fig.text(0.075, 0.905, "MOST FORM CLEAR MORPHOLOGICAL CLUSTERS. TWO SHARE MUCH OF THE SAME SPACE.", fontsize=14, fontweight="bold", color=text)
fig.text(0.075, 0.865, "PENGUIN MORPHOSPACE BASED ON TEN STANDARDIZED BODY MEASUREMENTS", fontsize=13, fontweight="bold", color=blue)
fig.text(0.075, 0.025, "Source: AVONET via TidyTuesday  |  Rowan Olson · #TidyTuesday", fontsize=9.5, color=muted)

plt.subplots_adjust(left=0.12, right=0.95, top=0.80, bottom=0.11)
plt.savefig("penguins.png", dpi=300, bbox_inches="tight", facecolor=bg)
plt.show()