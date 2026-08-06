import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("ultimate_ufc_dataset.csv")

bg = "#FFFFFF"
text = "#111111"
muted = "#666666"
grid = "#E2E2E2"
blue = "#264B73"
ko = "#B83A3A"
sub = "#D99C27"
decision = "#4B7F90"

order = ["Heavyweight", "Light Heavyweight", "Middleweight", "Welterweight", "Lightweight", "Featherweight", "Bantamweight", "Flyweight", "Women's Bantamweight", 
    "Women's Flyweight", "Women's Strawweight"]

d = df[["weight_class", "finish"]].dropna().copy()
d["finish_type"] = np.select([d["finish"].eq("KO/TKO"), d["finish"].eq("SUB"), d["finish"].isin(["U-DEC", "S-DEC", "M-DEC"])], ["Knockout", "Submission", "Decision"], 
    default="Other")
d = d[(d["finish_type"] != "Other") & d["weight_class"].isin(order)]

summary = pd.crosstab(d["weight_class"], d["finish_type"]).reindex(order).fillna(0)
summary["fights"] = summary.sum(axis=1)
summary[["Knockout", "Submission", "Decision"]] = summary[["Knockout", "Submission", "Decision"]].div(summary["fights"], axis=0) * 100
summary = summary.sort_values("Knockout", ascending=True)

fig, ax = plt.subplots(figsize=(14, 10), facecolor=bg)
ax.set_facecolor(bg)

y = np.arange(len(summary))

ax.barh(y, summary["Knockout"], color=ko, height=0.66)
ax.barh(y, summary["Submission"], left=summary["Knockout"], color=sub, height=0.66)
ax.barh(y, summary["Decision"], left=summary["Knockout"] + summary["Submission"], color=decision, height=0.66)

for i, (_, row) in enumerate(summary.iterrows()):
    ax.text(row["Knockout"] / 2, i, f'{row["Knockout"]:.0f}%', ha="center", va="center", fontsize=11, color="white", fontweight="bold")
    ax.text(row["Knockout"] + row["Submission"] / 2, i, f'{row["Submission"]:.0f}%', ha="center", va="center", fontsize=10.5, color=text, fontweight="bold")
    ax.text(row["Knockout"] + row["Submission"] + row["Decision"] / 2, i, f'{row["Decision"]:.0f}%', ha="center", va="center", fontsize=11, color="white", fontweight="bold")

ax.set_yticks(y)
ax.set_yticklabels(summary.index, fontsize=12, color=text, weight="bold")
ax.set_xlim(0, 112)
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%", "100%"], fontsize=10.5, color=muted)
ax.grid(axis="x", color=grid, linewidth=0.9)
ax.set_axisbelow(True)
ax.tick_params(axis="both", length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(0.075, 0.91, "EVERY UFC DIVISION HAS A DIFFERENT WAY TO WIN.", fontsize=28, fontweight="bold", color=text)
fig.text(0.075, 0.87, "KNOCKOUTS BECOME RARER IN LIGHTER DIVISIONS. SUBMISSIONS HARDLY CHANGE.", fontsize=14, fontweight="bold", color=text)
fig.text(0.075, 0.838, "SHARE OF COMPLETED UFC FIGHTS BY FINISH TYPE AND WEIGHT CLASS", fontsize=13, fontweight="bold", color=blue)

fig.text(0.25, 0.785, "KNOCKOUT", fontsize=11.5, fontweight="bold", color=ko)
fig.text(0.5, 0.785, "SUBMISSION", fontsize=11.5, fontweight="bold", color=sub)
fig.text(0.777, 0.785, "DECISION", fontsize=11.5, fontweight="bold", color=decision)

fig.text(0.075, 0.025, "Source: Ultimate UFC Dataset via TidyTuesday  |  Rowan Olson · #TidyTuesday", fontsize=9.5, color=muted)

plt.subplots_adjust(left=0.25, right=0.91, top=0.74, bottom=0.08)
plt.savefig("ufc.png", dpi=300, bbox_inches="tight", facecolor=bg)
plt.show()