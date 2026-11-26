"""Run from the repository root: python scripts/06_analysis/make_figures.py  -> figures/*.png and *.svg"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from statsmodels.stats.proportion import proportion_confint
BLUE, ORANGE, INK, INK2, GRID, SURF = '#257de0', '#f47230', '#191919', '#666666', '#e6e6e6', '#ffffff'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': INK, 'axes.edgecolor': GRID, 'axes.labelcolor': INK2,
                     'xtick.color': INK2, 'ytick.color': INK, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.facecolor': SURF})
d = pd.read_csv('data/coding/coding_final.csv', keep_default_na=False); X = pd.read_csv('data/coding/x6_three_judgments.csv').set_index('ft_id')
inc = d[d.ft_decision == 'include']; t12 = inc[inc.study_type != 'T3'].copy(); t12['GC'] = t12.ft_id.map(X.general_claim)
def save(fig, name):
    for ext in ('png', 'svg'): fig.savefig(f'figures/{name}.{ext}', dpi=200, bbox_inches='tight')
    plt.close(fig)
def bars(ax, labels, vals, color, fmt):
    y = np.arange(len(labels))[::-1]
    ax.barh(y, vals, height=0.62, color=color, linewidth=0)
    ax.set_yticks(y, labels); ax.tick_params(axis='y', length=0); ax.spines['left'].set_visible(False)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    for yi, v in zip(y, vals): ax.text(v + max(vals) * 0.015, yi, fmt(v), va='center', color=INK, fontsize=9)
# 1 PRISMA: drawn by its own script
import runpy; runpy.run_path('scripts/06_analysis/prisma_figure.py')
# 2 regime confusion
order = ['Answering', 'Customized assistant', 'Grounded/RAG', 'Tool-using agent', 'Autonomous/multi-agent', 'Unclear']
a = t12.X1.value_counts().reindex(order, fill_value=0); g = t12[t12.GC == 'Y'].X1.value_counts().reindex(order, fill_value=0)
fig, axs = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
bars(axs[0], order, a.values, BLUE, lambda v: f"{v}  ({100*v/a.sum():.0f}%)"); axs[0].set_title(f'All studies using or analysing AI outputs (n = {a.sum()})', loc='left', fontsize=10.5)
bars(axs[1], order, g.values, BLUE, lambda v: f"{v}  ({100*v/g.sum():.0f}%)"); axs[1].set_title(f'Studies drawing general conclusions about AI (n = {g.sum()})', loc='left', fontsize=10.5)
for ax in axs: ax.set_xlim(0, max(a) * 1.25); ax.set_xlabel('Number of studies')
fig.suptitle('Regime confusion: general claims about "AI" rest mostly on answering systems', x=0.01, ha='left', fontsize=12.5, fontweight='bold', y=1.04)
save(fig, 'fig2_regime_confusion')
# 3 reporting by item
NAMES = {'A1': 'A1 Role of the AI', 'A2': 'A2 Human-in-the-loop', 'B1': 'B1 Model version + date', 'B2': 'B2 Access mode', 'B3': 'B3 Parameters',
         'B4': 'B4 Prompts', 'B5': 'B5 Context / memory', 'C1': 'C1 Inputs', 'C2': 'C2 Repetitions', 'D1': 'D1 Data protection',
         'E1': 'E1 Human validation', 'E2': 'E2 Post-processing', 'F1': 'F1 Data/code availability', 'G1': 'G1 Funding + COI'}
rows = []
for it in NAMES:
    s = inc[~inc[it].isin(['NA'])]; rows.append((NAMES[it], 100 * (s[it] == 'R').mean(), 100 * (s[it] == 'P').mean(), len(s)))
R = pd.DataFrame(rows, columns=['item', 'R', 'P', 'n']).sort_values('R')
fig, ax = plt.subplots(figsize=(9, 5.6)); y = np.arange(len(R))
ax.barh(y, R.R, height=0.62, color=BLUE, edgecolor=SURF, linewidth=2, label='Fully reported')
ax.barh(y, R.P, left=R.R, height=0.62, color='#a8c9f0', edgecolor=SURF, linewidth=2, label='Partly reported')
ax.set_yticks(y, [f"{i}  (n = {k})" for i, k in zip(R.item, R.n)]); ax.tick_params(axis='y', length=0); ax.spines['left'].set_visible(False)
for yi, r, p in zip(y, R.R, R.P): ax.text(r + p + 1, yi, f"{r:.0f}% full", va='center', fontsize=8.5, color=INK)
ax.set_xlim(0, 112); ax.set_xlabel('% of studies where the item applies'); ax.xaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
ax.legend(loc='lower right', frameon=False, fontsize=9); ax.set_title('Reporting of GUIDE-LLM core items (included studies)', loc='left', fontsize=12, fontweight='bold')
save(fig, 'fig3_reporting_by_item')
# 4 hypotheses vs thresholds
H = [('H1  Report model version AND date', (inc.B1 == 'R').sum(), len(inc), 50, '< 50%'),
     ('H3  Study tool-using / autonomous AI', t12.X1.isin(['Tool-using agent', 'Autonomous/multi-agent']).sum(), len(t12), 10, '< 10%'),
     ('H4  Over-generalize without qualification', (t12.ft_id.map(X.X6) == 'yes').sum(), len(t12), 25, '> 25%')]
fig, ax = plt.subplots(figsize=(9, 2.9)); yy = np.arange(len(H))[::-1]
for yi, (lab, k, n_, thr, sign) in zip(yy, H):
    lo, hi = proportion_confint(k, n_, method='wilson'); p = 100 * k / n_
    ax.plot([100 * lo, 100 * hi], [yi, yi], color=BLUE, lw=2, solid_capstyle='round'); ax.plot(p, yi, 'o', ms=9, color=BLUE, mec=SURF, mew=2)
    ax.plot([thr, thr], [yi - 0.3, yi + 0.3], color=INK, lw=1.6); ax.text(thr, yi + 0.34, f'predicted {sign}', ha='center', fontsize=8, color=INK2)
    ax.text((100 * hi if thr - 100 * hi > 15 else max(100 * hi, thr)) + 1.5, yi, f'{p:.1f}%  ({k}/{n_})', va='center', fontsize=9)
ax.set_yticks(yy, [h[0] for h in H]); ax.tick_params(axis='y', length=0); ax.spines['left'].set_visible(False)
ax.set_xlim(0, 62); ax.set_ylim(-0.6, 2.75); ax.set_xlabel('% of studies (dot = estimate, line = 95% Wilson CI, black tick = pre-registered threshold)')
ax.xaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True); ax.set_title('Pre-registered hypotheses: H1 and H3 supported, H4 not supported', loc='left', fontsize=12, fontweight='bold')
save(fig, 'fig4_hypotheses')
# 5 by field
F = pd.read_csv('data/screening/fulltext_list.csv').set_index('ft_id'); t12['field'] = t12.ft_id.map(F.field); inc2 = inc.assign(field=inc.ft_id.map(F.field))
fo = ['Communication and media', 'Education', 'Health and psychology', 'Human-computer interaction', 'Social sciences']
x6 = [100 * (t12[t12.field == f].ft_id.map(X.X6) == 'yes').mean() for f in fo]; b1 = [100 * (inc2[inc2.field == f].B1 == 'R').mean() for f in fo]
fig, axs = plt.subplots(1, 2, figsize=(11, 3.4), sharey=True)
bars(axs[0], fo, b1, BLUE, lambda v: f"{v:.0f}%"); axs[0].set_title('Report model version + date (all included)', loc='left', fontsize=10.5)
bars(axs[1], fo, x6, BLUE, lambda v: f"{v:.0f}%"); axs[1].set_title('Over-generalize without qualification (T1+T2)', loc='left', fontsize=10.5)
for ax in axs: ax.set_xlim(0, 45); ax.set_xlabel('% of studies')
fig.suptitle('By field', x=0.01, ha='left', fontsize=12.5, fontweight='bold', y=1.03)
save(fig, 'fig5_by_field')
print('figures written')
