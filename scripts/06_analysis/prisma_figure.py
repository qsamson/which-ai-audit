"""Run from the repository root: python scripts/06_analysis/prisma_figure.py -> figures/fig1_prisma.png/.svg"""
import pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
P = pd.read_csv('data/screening/prisma_final.csv'); P['k'] = P.iloc[:, 0].str.strip()
cut = P.index[P.k == 'Full texts sought'][0]
a = dict(zip(P.k[:cut], P.n[:cut])); b = dict(zip(P.k[cut:], P.n[cut:]))
INK, WHITE = '#2b1a12', '#ffffff'
STAGE = {'Identification': '#c2410c', 'Screening': '#ea580c', 'Eligibility': '#f59e0b', 'Included': '#dc2626'}
MAIN_FC, MAIN_EC = '#ffedd5', '#ea580c'
EXC_FC, EXC_EC = '#fffaf2', '#f59e0b'
INC_FC, INC_EC = '#fde3e1', '#dc2626'
rows = [  # (stage, main text, exclusion text or None)
 ('Identification', f"Records identified via OpenAlex\n15 journals, 2023–2026\nn = {a['Records identified (OpenAlex, 15 journals, 2023–2026)']:,}", f"Duplicates removed\nn = {a['Duplicates removed']}"),
 ('Identification', f"Records after duplicates removed\nn = {a['Records identified (OpenAlex, 15 journals, 2023–2026)'] - a['Duplicates removed']:,}",
  f"Not screened: stopping rule reached\n20 inclusions per journal,\nfixed random order\nn = {a['Not screened (fixed random order; stopping rule of 20 includes per journal)']:,}"),
 ('Screening', f"Records screened\ntitle and abstract\nn = {a['Records screened (title/abstract)']}",
  f"Records excluded, n = {a['Excluded at title/abstract']}\nE1 not empirical: {a['E1 not empirical']}\nE2 not generative AI: {a['E2 not generative AI']}\nE3 AI only as research tool: {a['E3 GenAI only as research tool']}\nE6 no real AI output: {a['E6 no real AI output']}\nRetracted: {a['Retracted']}"),
 ('Eligibility', f"Full texts sought\nn = {b['Full texts sought']}", f"Full texts not retrieved\nE4 inaccessible\nn = {b['Not retrieved (E4, full text inaccessible)']}"),
 ('Eligibility', f"Full texts assessed\nn = {b['Full texts assessed']}",
  f"Full texts excluded, n = {b['Excluded at full text']}\nE2 not generative AI: {b['E2 not generative AI']}\nE6 no real AI output: {b['E6 no real AI output']}\nE1 not empirical: {b['E1 not empirical']}"),
 ('Included', f"Studies included\nn = {b['Included']}\n\nT1 researcher-controlled AI use: {b['T1 researcher-controlled AI use']}\nT2 analysis of existing AI outputs: {b['T2 analysis of existing AI outputs']}\nT3 participant-reported use: {b['T3 participant-reported use']}", None)]
LH, PAD, GAP = 0.34, 0.42, 0.35          # line height, vertical padding, gap between rows (inches-as-units)
SX, SW, MX, MW, EX, EW = 0.0, 0.55, 0.85, 4.3, 5.75, 4.3
H = [max(t.count('\n') + 1, (e.count('\n') + 1) if e else 0) * LH + PAD for _, t, e in rows]
total = sum(H) + GAP * (len(rows) - 1)
fig = plt.figure(figsize=(EX + EW + 0.2, total + 0.9)); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(-0.1, EX + EW + 0.1); ax.set_ylim(-0.75, total + 0.15); ax.axis('off')
def box(x, y, w, h, fc, ec, lw=1.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=0.14', fc=fc, ec=ec, lw=lw))
def text(x, y, s, **k):
    lines = s.split('\n'); first, rest = lines[0], '\n'.join(lines[1:])
    return ax.text(x, y, s, ha='center', va='center', color=INK, fontsize=11.5, linespacing=1.45, **k)
y = total; ys = []; texts = []; mids = []
for (stage, t, e), h in zip(rows, H):
    y0 = y - h; ys.append((stage, y0, y))
    inc = stage == 'Included'
    mh = (t.count('\n') + 1) * LH + PAD; my = y0 + (h - mh) / 2; mids.append((my, my + mh))
    box(MX, my, MW, mh, INC_FC if inc else MAIN_FC, INC_EC if inc else MAIN_EC, 2.2 if inc else 1.8)
    texts.append((text(MX + MW / 2, my + mh / 2, t, fontweight='bold' if inc or t.startswith('Records identified') else 'normal'), MX, MW, my, mh))
    if e:
        eh = (e.count('\n') + 1) * LH + PAD; ey = y0 + (h - eh) / 2
        box(EX, ey, EW, eh, EXC_FC, EXC_EC)
        texts.append((text(EX + EW / 2, ey + eh / 2, e), EX, EW, ey, eh))
        ax.annotate('', (EX, y0 + h / 2), (MX + MW, y0 + h / 2), arrowprops=dict(arrowstyle='-|>,head_width=0.35,head_length=0.6', color=EXC_EC, lw=2))
    y = y0 - GAP
for (a0, a1), (b0, b1) in zip(mids, mids[1:]):
    ax.annotate('', (MX + MW / 2, b1), (MX + MW / 2, a0), arrowprops=dict(arrowstyle='-|>,head_width=0.35,head_length=0.6', color=MAIN_EC, lw=2))
# stage bars
for st in STAGE:
    r = [(y0, y1) for s, y0, y1 in ys if s == st]
    lo, hi = min(r)[0], max(x[1] for x in r)
    box(SX, lo, SW, hi - lo, STAGE[st], STAGE[st], 0)
    ax.text(SX + SW / 2, (lo + hi) / 2, st, rotation=90, ha='center', va='center', color=WHITE, fontsize=12, fontweight='bold')
ax.text(MX, -0.45, 'Screening followed a fixed random order per journal and stopped at 20 inclusions; later records were not screened.',
        ha='left', va='center', fontsize=9.5, color='#7c4a2d', style='italic')
# fit check: every text must sit inside its box with a margin
fig.canvas.draw(); r = fig.canvas.get_renderer(); inv = ax.transData.inverted(); bad = 0
for t, x, w, y0, h in texts:
    bb = inv.transform(t.get_window_extent(r)); (x1, y1), (x2, y2) = bb
    if x1 < x + 0.12 or x2 > x + w - 0.12 or y1 < y0 + 0.08 or y2 > y0 + h - 0.08: bad += 1; print('DOES NOT FIT:', t.get_text()[:40])
for ext in ('png', 'svg'): fig.savefig(f'figures/fig1_prisma.{ext}', dpi=200, facecolor=WHITE)
print('PRISMA written; boxes that do not fit:', bad)
