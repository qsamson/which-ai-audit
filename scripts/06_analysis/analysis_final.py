"""Run from the repository root:  python scripts/06_analysis/analysis_final.py
Which AI? — final pre-specified analyses. Input: coded_final.pkl, x6_final.csv, which_ai_master_screening.xlsx"""
import pandas as pd, numpy as np, itertools
from scipy.stats import binomtest, kruskal, norm, rankdata, fisher_exact, chi2_contingency
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.multitest import multipletests
import statsmodels.formula.api as smf
rng = np.random.default_rng(2027)
d = pd.read_csv('data/coding/coding_final.csv', keep_default_na=False); X = pd.read_csv('data/coding/x6_three_judgments.csv').set_index('ft_id')
F = pd.read_csv('data/screening/fulltext_list.csv').set_index('ft_id')
J = pd.read_csv('data/screening/by_journal.csv').set_index('Journal')
inc = d[d.ft_decision == 'include'].copy().drop(columns=['journal','field','year','title','doi'],errors='ignore'); inc['journal'] = inc.ft_id.map(F.journal); inc['field'] = inc.journal.map(J.Field)
inc['X6'] = inc.ft_id.map(X.X6).where(inc.study_type != 'T3', 'NA')
t12 = inc[inc.study_type != 'T3']
out = []
def W(k, n): lo, hi = proportion_confint(k, n, method='wilson'); return f"{k}/{n} ({100*k/n:.1f}%; 95% CI {100*lo:.1f}–{100*hi:.1f})"
# H1
k = (inc.B1 == 'R').sum(); n = len(inc); p = binomtest(k, n, 0.5, alternative='less').pvalue
out.append(('H1', '<50% report model version AND date', W(k, n), f"one-sided binomial vs 0.50, p = {p:.2g}", 'supported' if p < .05 else 'not supported'))
# H3
k = t12.X1.isin(['Tool-using agent', 'Autonomous/multi-agent']).sum(); n = len(t12); p = binomtest(k, n, 0.10, alternative='less').pvalue
out.append(('H3', '<10% study tool-using/autonomous AI', W(k, n), f"one-sided binomial vs 0.10, p = {p:.2g}", 'supported' if p < .05 else 'not supported'))
# H4
k = (t12.X6 == 'yes').sum(); p = binomtest(k, n, 0.25, alternative='greater').pvalue; p2 = binomtest(k, n, 0.25, alternative='less').pvalue
out.append(('H4', '>25% over-generalize (X6)', W(k, n), f"one-sided binomial vs 0.25 (greater), p = {p:.2f}; (less) p = {p2:.3f}", 'supported' if p < .05 else 'not supported (rate significantly BELOW 25%)' if p2 < .05 else 'not supported'))
# H2: reporting completeness score over the 14 core items that apply (R=1, P=.5, N=0)
CORE = ['A1','A2','B1','B2','B3','B4','B5','C1','C2','D1','E1','E2','F1','G1']; V = {'R': 1, 'P': .5, 'N': 0}
inc['score'] = inc[CORE].apply(lambda r: np.mean([V[x] for x in r if x in V]), axis=1)
groups = [g.score.values for _, g in inc.groupby('field')]; H, pk = kruskal(*groups)
out.append(('H2', 'reporting differs across fields', 'median score by field: ' + '; '.join(f"{f} {g.median():.2f}" for f, g in inc.groupby('field').score), f"Kruskal–Wallis H = {H:.2f}, df = 4, p = {pk:.2g}", 'supported' if pk < .05 else 'not supported'))
# Dunn post hoc, Holm
r = rankdata(inc.score); N = len(r); inc['rk'] = r; tie = 1 - sum(c**3 - c for c in np.unique(r, return_counts=True)[1]) / (N**3 - N)
pairs = []; fs = sorted(inc.field.unique())
for a, b in itertools.combinations(fs, 2):
    A, B = inc[inc.field == a], inc[inc.field == b]
    z = (A.rk.mean() - B.rk.mean()) / np.sqrt(tie * N * (N + 1) / 12 * (1/len(A) + 1/len(B))); pairs.append((a, b, z, 2 * norm.sf(abs(z))))
P = pd.DataFrame(pairs, columns=['field_a', 'field_b', 'z', 'p']); P['p_holm'] = multipletests(P.p, method='holm')[1]
# per item: field x (R vs not) — Fisher–Freeman–Halton via Monte Carlo permutation of chi-square, Holm
def perm_p(f, y, B=10000):
    codes, f = np.unique(f, return_inverse=True); nf = np.bincount(f); p = y.mean()
    def chi(yy):
        k = np.bincount(f, weights=yy.astype(float)); e = nf * p; return (((k - e)**2) / e + ((nf - k - nf*(1-p))**2) / (nf*(1-p))).sum()
    o = chi(y); c = sum(chi(rng.permutation(y)) >= o - 1e-12 for _ in range(B)); return (c + 1) / (B + 1)
IT = []
for it in CORE + ['X6']:
    s = inc[~inc[it].isin(['NA'])] if it != 'X6' else t12
    y = (s[it] == ('yes' if it == 'X6' else 'R')).values
    if y.sum() in (0, len(y)): IT.append((it, len(s), y.sum(), np.nan)); continue
    IT.append((it, len(s), int(y.sum()), perm_p(s.field.values, y)))
IT = pd.DataFrame(IT, columns=['item', 'n', 'n_R_or_yes', 'p_perm']); m = IT.p_perm.notna(); IT.loc[m, 'p_holm'] = multipletests(IT.p_perm[m], method='holm')[1]
byf = inc.groupby('field').apply(lambda g: pd.Series({**{it: f"{(g[it]=='R').sum()}/{(~g[it].isin(['NA'])).sum()}" for it in CORE}, 'X6 yes': f"{(g.X6=='yes').sum()}/{(g.study_type!='T3').sum()}", 'median score': round(g.score.median(), 2)}))
# regression with journal-clustered SEs
inc['year'] = inc.ft_id.map(F.year) if 'year' in F.columns else np.nan
fml = 'score ~ C(field) + C(study_type)' + (' + year' if inc.year.notna().all() else '')
reg = smf.ols(fml, data=inc).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(inc.journal)[0]})
# sensitivity: journals where all records were screened vs sampled to 20; and by full-text retrieval rate
inc['all_screened'] = inc.journal.map(J['Reached 20?']).str.startswith('no')
sought = F.groupby('journal').size(); got = d.assign(j=d.ft_id.map(F.journal)).groupby('j').size(); rate = (got / sought).fillna(0)
inc['high_retrieval'] = inc.journal.map(rate) >= 0.8; t12 = inc[inc.study_type != 'T3']
SENS = []
for lab, col in [('All records screened', 'all_screened'), ('Full-text retrieval >= 80%', 'high_retrieval')]:
    for v in (True, False):
        a = inc[inc[col] == v]; b = t12[t12[col] == v]
        SENS.append((lab, 'yes' if v else 'no', W((a.B1=='R').sum(), len(a)), W((b.X6=='yes').sum(), len(b)), W(b.X1.isin(['Tool-using agent','Autonomous/multi-agent']).sum(), len(b))))
SENS = pd.DataFrame(SENS, columns=['subset', 'value', 'H1: B1 = R', 'H4: X6 yes', 'H3: agentic'])
DESC = pd.DataFrame([('General AI claim (T1+T2)', W((X.loc[t12.ft_id].general_claim=='Y').sum(), len(t12))),
                     ('Model/version caveat stated (T1+T2)', W((X.loc[t12.ft_id].model_version_caveat=='Y').sum(), len(t12))),
                     ('Authors disclose own LLM use (R)', W(inc.R.str.startswith('disclosed').sum(), len(inc))),
                     ('Regimes (T1+T2)', '; '.join(f"{k} {v}" for k, v in t12.X1.value_counts().items())),
                     ('Study types', '; '.join(f"{k} {v}" for k, v in inc.study_type.value_counts().sort_index().items()))], columns=['measure', 'result'])
HYP = pd.DataFrame(out, columns=['hypothesis', 'statement', 'estimate', 'test', 'verdict'])
with pd.ExcelWriter('results/which_ai_results_reproduced.xlsx') as w:
    HYP.to_excel(w, sheet_name='Hypotheses', index=False); DESC.to_excel(w, sheet_name='Descriptives', index=False); byf.to_excel(w, sheet_name='By field')
    IT.to_excel(w, sheet_name='Items by field (H2)', index=False); P.to_excel(w, sheet_name='Dunn post hoc (H2)', index=False)
    pd.DataFrame({'coef': reg.params, 'se_cluster': reg.bse, 'p': reg.pvalues}).to_excel(w, sheet_name='Regression (H2)'); SENS.to_excel(w, sheet_name='Sensitivity', index=False)
pd.set_option('display.width', 250, 'display.max_colwidth', 120)
print(HYP.to_string(index=False)); print(DESC.to_string(index=False)); print(byf.to_string()); print(IT.round(4).to_string(index=False)); print(P.round(4).to_string(index=False))
print(reg.summary().tables[1]); print('formula:', fml); print(SENS.to_string(index=False))
# H2 restricted to T1+T2 (the T3 score uses only 4 items, so mixing types confounds the field comparison)
for lab, s in [('T1+T2', inc[inc.study_type != 'T3']), ('T1 only', inc[inc.study_type == 'T1'])]:
    Hs, ps = kruskal(*[g.score.values for _, g in s.groupby('field')])
    print(f"H2 sensitivity {lab}: n={len(s)}, KW H={Hs:.2f}, p={ps:.3f}; medians", s.groupby('field').score.median().round(2).to_dict())
