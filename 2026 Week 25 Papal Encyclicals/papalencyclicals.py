import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load data
folder = Path(__file__).parent
df = pd.read_csv(folder / "papal_encyclicals.csv")

# Count encyclicals per year by pope
year_pope_counts = (
    df.groupby(["year", "pope"])
      .size()
      .reset_index(name="count")
)

stacked = (
    year_pope_counts
    .pivot(index="year", columns="pope", values="count")
    .fillna(0)
    .sort_index()
)

# Plot settings
plt.rcParams["font.family"] = "DejaVu Sans"

pope_colors = {
    "Leo XIII": "#2E7D32",
    "Pius X": "#7B3294",
    "Benedict XV": "#2166AC",
    "Pius XI": "#1B9E9E",
    "Pius XII": "#A65E2E",
    "John XXIII": "#4D9221",
    "Paul VI": "#C44E52",
    "John Paul II": "#E6862A",
    "Benedict XVI": "#7FA6D9",
    "Francis": "#D73027",
    "Leo XIV": "#5E3C99",
}

eras = [
    (1878, 1914, "Print Era\n~1914 and Earlier", "#DDE8D5"),
    (1914, 1945, "Radio / Broadcast Era\n~1914-1945", "#D9E6F2"),
    (1945, 1995, "Television Era\n~1945-1995", "#F2E3D5"),
    (1995, 2027, "Internet Era\n~1995-Present", "#E6DDF2"),
]

fig, ax = plt.subplots(figsize=(16, 8))

# Era background bands
for start, end, label, color in eras:
    ax.axvspan(
        start,
        end,
        color=color,
        alpha=0.55,
        zorder=0
    )

    ax.text(
        (start + end) / 2,
        7.65,
        label,
        ha="center",
        va="top",
        fontsize=9,
        fontweight="bold",
        color="#444444",
        zorder=3
    )

# Bars
for pope in stacked.columns:
    pope_data = stacked[pope]
    years = pope_data[pope_data > 0].index
    counts = pope_data[pope_data > 0].values

    ax.bar(
        years,
        counts,
        width=0.75,
        label=pope,
        color=pope_colors.get(pope, "#999999"),
        alpha=0.95,
        zorder=2
    )

# Title
ax.set_title(
    "Why Have Papal Encyclicals Become So Rare?",
    fontsize=38,
    fontweight="bold",
    pad=34
)

ax.text(
    0.5,
    1.015,
    "Annual papal encyclical publication by year (1878–2026)",
    transform=ax.transAxes,
    ha="center",
    va="bottom",
    fontsize=14,
    color="#555555"
)

ax.set_xlabel("Publication Year", fontsize=13, labelpad=1)
ax.set_ylabel("Number of Encyclicals Published", fontsize=13)

# Axes formatting
ax.set_xlim(1878, 2027)
ax.set_ylim(0, 8.6)

ax.set_xticks(range(1880, 2031, 10))
ax.tick_params(axis="x", rotation=45, labelsize=10)
ax.tick_params(axis="y", labelsize=10)

ax.grid(axis="y", alpha=0.3, zorder=1)
ax.grid(axis="x", alpha=0)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend
legend = ax.legend(
    title="Pope",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    frameon=False,
    fontsize=9,
    title_fontsize=11
)

legend.get_frame().set_alpha(0.94)
legend.get_frame().set_edgecolor("#CCCCCC")

# Credits
fig.text(
    0.01,
    0.003,
    "TidyTuesday • Week 25 (2026) | Data: Vatican.va | Analysis & Visualization: Rowan Olson | #TidyTuesday",
    ha="left",
    va="bottom",
    fontsize=10,
    color="#777777"
)

plt.savefig(folder / "papalencyclicals.png",dpi=300,bbox_inches="tight",facecolor="white")
plt.tight_layout()
plt.show()