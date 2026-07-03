import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# Load data
# -----------------------------
folder = Path(__file__).parent
df = pd.read_csv(folder / "wreck_inventory.csv")

# -----------------------------
# Clean / prepare
# -----------------------------
df = df[df["year"].notna()].copy()
df["year"] = df["year"].astype(int)

# Start at 1700
df = df[df["year"] >= 1700].copy()

# Remove generic / less useful classifications
excluded_classes = [
    "Unknown",
    "Ship",
    "Boat",
    "Sailing Ship",
    "Fishing boat"
]

class_counts = (
    df[df["classification"].notna()]
    .query("classification not in @excluded_classes")
    ["classification"]
    .value_counts()
)

top_classes = class_counts.head(8).index

plot_df = df[df["classification"].isin(top_classes)].copy()
plot_df["decade"] = (plot_df["year"] // 10) * 10

decade_counts = (
    plot_df.groupby(["classification", "decade"])
    .size()
    .reset_index(name="wrecks")
)

all_decades = range(1700, plot_df["decade"].max() + 10, 10)

decade_counts = (
    decade_counts
    .pivot(index="decade", columns="classification", values="wrecks")
    .reindex(all_decades)
    .fillna(0)
)

# Reorder ship types by median wreck year
class_order = (
    plot_df.groupby("classification")["year"]
    .median()
    .sort_values()
    .index
)

# Normalize each ship type to its own peak
normalized_counts = decade_counts.copy()

for ship_type in normalized_counts.columns:
    peak = normalized_counts[ship_type].max()
    if peak > 0:
        normalized_counts[ship_type] = normalized_counts[ship_type] / peak

# Total n for labels
class_n = plot_df["classification"].value_counts()

# -----------------------------
# Plot
# -----------------------------
plt.rcParams["font.family"] = "DejaVu Sans"

main_color = "#24476D"

fig, axes = plt.subplots(
    nrows=len(class_order),
    ncols=1,
    figsize=(12, 8),
    sharex=True
)

for ax, ship_type in zip(axes, class_order):
    y = normalized_counts[ship_type]

    ax.fill_between(
        normalized_counts.index,
        y,
        color=main_color,
        alpha=0.82
    )

    ax.plot(
        normalized_counts.index,
        y,
        color=main_color,
        linewidth=1.5
    )

    ax.text(
        0.01,
        0.65,
        ship_type,
        transform=ax.transAxes,
        ha="left",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#222222"
    )

    ax.text(
        0.985,
        0.65,
        f"n = {class_n[ship_type]:,}",
        transform=ax.transAxes,
        ha="right",
        va="center",
        fontsize=9,
        color="#999999"
    )

    ax.set_ylim(0, 1.12)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.spines["bottom"].set_linewidth(0.8)

    ax.tick_params(axis="y", left=False, labelleft=False)
    ax.grid(axis="x", color="#ECECEC", linewidth=0.8)

# -----------------------------
# Title / labels
# -----------------------------
fig.text(
    0.5,
    0.985,
    "THE AGE OF SAIL GAVE WAY TO STEAM",
    ha="center",
    va="top",
    fontsize=28,
    fontweight="bold",
    color="black"
)

fig.text(
    0.5,
    0.945,
    "COMMON VESSEL TYPES IN IRISH SHIPWRECKS SHIFTED DRAMATICALLY DURING THE 1800s",
    ha="center",
    va="top",
    fontsize=14,
    fontweight="bold",
    color="#24476D"
)

fig.text(
    0.5,
    0.918,
    "Normalized wreck frequency by vessel classification and decade of loss (1700–present)",
    ha="center",
    va="top",
    fontsize=12,
    color="#666666"
)

axes[-1].set_xlabel(
    "Year of wreck",
    fontsize=12,
    labelpad=10
)

# -----------------------------
# Credits
# -----------------------------
fig.text(
    0.01,
    0.01,
    "TidyTuesday • Week 26 (2026) | Data: Wreck Inventory of Ireland Database | Analysis & Visualization: Rowan Olson | #TidyTuesday",
    ha="left",
    va="bottom",
    fontsize=8,
    color="#777777"
)

plt.tight_layout(rect=[0, 0.04, 1, 0.90])

plt.savefig(
    folder / "wrecks.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.show()