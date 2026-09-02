import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

df = pd.read_csv('world_castles.csv')
df = df.dropna(subset=['country', 'pageviews']).query('pageviews > 0').copy()

country = df.groupby('country').agg(castles=('name', 'size'), median_views=('pageviews', 'median')).reset_index()
country = country.query('castles >= 50').copy()

BG = '#FAF9F6'
TEXT = '#272522'
MUTED = '#8B8984'
GRID = '#DEDCD6'
ACCENT = '#C14D34'
POINT = '#AAA59C'

fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.scatter(country['castles'], country['median_views'], s=70, color=POINT, edgecolor=BG, linewidth=1.2, zorder=3)

highlight = ['United States', 'England', 'Scotland', 'India', 'France', 'Germany', 'Italy']
h = country[country['country'].isin(highlight)]
ax.scatter(h['castles'], h['median_views'], s=80, color=ACCENT, edgecolor=BG, linewidth=1.2, zorder=4)

offsets = {
    'United States': (8, 8),
    'England': (8, 8),
    'Scotland': (8, 8),
    'India': (8, 8),
    'Germany': (-57, 8),
    'Italy': (-12, 8),
    'France': (8, -16)
}

for _, r in h.iterrows():
    ax.annotate(r['country'], (r['castles'], r['median_views']), xytext=offsets[r['country']], textcoords='offset points', fontsize=9.5, fontweight='bold', color=TEXT)

ax.text(0, 1.105, 'MORE CASTLES DON’T MEAN MORE ATTENTION', transform=ax.transAxes, fontsize=22, fontweight='bold', color=TEXT, ha='left')
ax.text(0, 1.057, 'Countries with the largest castle collections often have much lower Wikipedia attention per structure.', transform=ax.transAxes, fontsize=11.5, color=TEXT, ha='left')
ax.text(0, 1.018, 'Countries with at least 50 structures in the dataset', transform=ax.transAxes, fontsize=9.5, color=MUTED, ha='left')

ax.set_xlabel('Structures in dataset', fontsize=10, color=MUTED, labelpad=10)
ax.set_ylabel('Median Wikipedia pageviews', fontsize=10, color=MUTED, labelpad=10)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))

ax.grid(True, color=GRID, linewidth=.8)
ax.set_axisbelow(True)
ax.tick_params(axis='both', colors=MUTED, labelsize=9, length=0)
for spine in ax.spines.values(): spine.set_visible(False)

ax.text(1, -.09, 'Source: TidyTuesday  •  world_castles', transform=ax.transAxes, fontsize=8, color=MUTED, ha='right')

plt.subplots_adjust(left=.11, right=.96, bottom=.12, top=.81)
plt.savefig('castles.png', dpi=300, bbox_inches='tight', facecolor=BG)
plt.show()