import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("nde_experiences.csv")

bg = "#FFFFFF"
text = "#111111"
muted = "#666666"
grid = "#E2E2E2"
blue = "#264B73"
purple = "#6047A6"
light_purple = "#D9D2EB"

features = {
    "ai_clinical": "Clinical death",
    "ai_obe": "Out-of-body",
    "ai_unity": "Unity",
    "ai_esp": "ESP",
    "ai_hellish": "Hellish",
    "ai_world_future": "Future visions",
    "ai_past_lives": "Past lives",
    "ai_aliens": "Aliens"
}

d = df[list(features)].fillna(False).astype(bool)

summary = pd.DataFrame({
    "feature": [features[column] for column in features],
    "reports": [int(d[column].sum()) for column in features],
    "share": [d[column].mean() * 100 for column in features]
})

summary = summary.sort_values("share", ascending=True).reset_index(drop=True)
summary["color"] = np.where(summary["share"] >= 50, purple, light_purple)

fig, ax = plt.subplots(figsize=(13, 9), facecolor=bg)
ax.set_facecolor(bg)

y = np.arange(len(summary))

ax.axvspan(0, 50, color="#F5F5F5", zorder=0)
ax.axvline(50, color=blue, linewidth=2, linestyle="--", zorder=1)
ax.barh(y, summary["share"], color=summary["color"], height=0.62, zorder=2)

ax.set_xlim(0, 105)

for i, row in summary.iterrows():
    value_color = purple if row["share"] >= 50 else text
    value_x = row["share"] + 1.2
    ax.text(value_x, i, f'{row["share"]:.0f}%', ha="left", va="center", fontsize=12, fontweight="bold", color=value_color)
    ax.text(104, i, f'{row["reports"]:,} reports', ha="right", va="center", fontsize=9.5, color=muted)

ax.text(60, len(summary) - 0.1, "MAJORITY OF REPORTS", ha="right", va="bottom", fontsize=10.5, fontweight="bold", color=blue)
ax.text(25, -0.5, "REPORTED IN A MINORITY OF CASES", ha="center", va="center", fontsize=10.5, fontweight="bold", color=muted)

ax.annotate(
    "Only two detected features\nappear in most reports",
    xy=(50, 5.75),
    xytext=(63, 4.85),
    ha="left",
    va="center",
    fontsize=11.5,
    fontweight="bold",
    color=blue,
    arrowprops=dict(arrowstyle="-", color=blue, linewidth=1.2)
)

ax.set_yticks(y)
ax.set_yticklabels(summary["feature"], fontsize=12, fontweight="bold", color=text)
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=10.5, color=muted)
ax.grid(axis="x", color=grid, linewidth=0.9)
ax.set_axisbelow(True)
ax.tick_params(axis="both", length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(0.075, 0.955, 'THE "CLASSIC" NEAR-DEATH EXPERIENCE ISN\'T TYPICAL.', fontsize=27, fontweight="bold", color=text)
fig.text(0.075, 0.905, "MOST EXTRAORDINARY PHENOMENA APPEAR IN ONLY A SMALL MINORITY OF REPORTS.", fontsize=14, fontweight="bold", color=text)
fig.text(0.075, 0.865, "SHARE OF 589 NDERF REPORTS CONTAINING EACH AI-DETECTED FEATURE", fontsize=13, fontweight="bold", color=blue)
fig.text(0.075, 0.025, "Source: Near Death Experience Research Foundation via TidyTuesday  |  Rowan Olson · #TidyTuesday", fontsize=9.5, color=muted)

plt.subplots_adjust(left=0.23, right=0.93, top=0.79, bottom=0.10)
plt.savefig("nderf.png", dpi=300, bbox_inches="tight", facecolor=bg)
plt.show()