"""Run from the repository root: python scripts/06_analysis/regime_confusion.py
Regime confusion: which interaction regimes underlie studies that draw general conclusions about AI."""
import pandas as pd
d = pd.read_pickle('data/coding/coded_final.pkl'); X = pd.read_csv('data/coding/x6_three_judgments.csv').set_index('ft_id')
t = d[(d.ft_decision == 'include') & (d.study_type != 'T3')].copy()
t['general_claim'] = t.ft_id.map(X.general_claim); t['X6'] = t.ft_id.map(X.X6)
AG = ['Tool-using agent', 'Autonomous/multi-agent']
def show(lab, s):
    n = len(s); a = (s.X1 == 'Answering').sum(); g = s.X1.isin(AG).sum()
    print(f"{lab}: n = {n}; answering only {a} ({100*a/n:.1f}%); tool-using/autonomous {g} ({100*g/n:.1f}%)")
    print('   ', s.X1.value_counts().to_dict())
show('Studies using/analysing AI outputs (T1+T2)', t)
show('Of these, studies drawing general conclusions about AI', t[t.general_claim == 'Y'])
show('Of these, unqualified over-generalization (X6 = yes)', t[t.X6 == 'yes'])
