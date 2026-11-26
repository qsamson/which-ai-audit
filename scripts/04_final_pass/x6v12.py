import pandas as pd, numpy as np
from scipy.stats import binomtest
from statsmodels.stats.proportion import proportion_confint as ci
from mkq import q
from spec_x6v12 import CH, YES, GC_N, MV_Y
d = pd.read_pickle('coded_v11.pkl'); s = d[(d.ft_decision=='include')&(d.study_type!='T3')].copy()
F=pd.read_excel('which_ai_master_screening.xlsx',sheet_name='Full-text list').set_index('ft_id'); J=pd.read_excel('which_ai_master_screening.xlsx',sheet_name='By journal').set_index('Journal').Field
rows=[]
for _,r in s.iterrows():
    f=r.ft_id; x6='yes' if f in YES else 'no'
    gc='N' if f in GC_N else 'Y'; mv='Y' if f in MV_Y else 'N'
    if f in CH: x6,gc,mv,sc,p=CH[f]
    else: sc = 'N' if x6=='yes' or gc=='N' else ('Y' if mv=='N' else '')
    qu = q(f,CH[f][4]) if f in CH and CH[f][4] else (r.X6_q if (x6==r.X6) else '')
    rows.append(dict(ft_id=f,field=J[F.journal[f]],type=r.study_type,general_claim=gc,model_version_caveat=mv,setup_caveat=sc,X6=x6,X6_v11=r.X6,X6_quote=qu))
X=pd.DataFrame(rows); assert set(X[X.X6=='yes'].ft_id)==set(YES)
bad=X[(X.X6=='yes')&((X.general_claim=='N')|(X.model_version_caveat=='Y'))]; print('inconsistent yes:',bad.ft_id.tolist())
X.to_csv('x6_v12_three_judgments.csv',index=False)
n=len(X)
def rep(k,lab):
    lo,hi=ci(k,n,method='wilson'); print(f"{lab}: {k}/{n} ({100*k/n:.1f}%, 95% CI {100*lo:.1f}–{100*hi:.1f})")
rep((X.general_claim=='Y').sum(),'General AI claim'); rep((X.model_version_caveat=='Y').sum(),'Model/version caveat'); k=(X.X6=='yes').sum(); rep(k,'X6 yes (H4)')
print('H4 one-sided binomial vs 0.25 (greater): p =',round(binomtest(k,n,0.25,alternative='greater').pvalue,4),'| (less): p =',round(binomtest(k,n,0.25,alternative='less').pvalue,4))
print('Among general-claim papers, X6 yes:',k,'/',(X.general_claim=='Y').sum())
print(X.groupby('field').apply(lambda g: f"{(g.X6=='yes').sum()}/{len(g)} ({100*(g.X6=='yes').mean():.0f}%)").to_string())
dc=pd.read_csv('double_coding_ids.csv').ft_id; sub=X[X.ft_id.isin(dc)]; print('subset yes:',sub[sub.X6=='yes'].ft_id.tolist(),'of',len(sub))
