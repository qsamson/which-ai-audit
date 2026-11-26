"""Adjudication round 2 (first author, 26 Nov 2026): 19 decisions + 10-paper spot-check -> coded_final.pkl"""
import re, pandas as pd
from mkq import T, q
d = pd.read_pickle('coded_v12.pkl').copy(); g = pd.read_pickle('reliability/gpt.pkl').set_index('ft_id')
A = pd.read_excel('data/coding/adjudication_round2_decisions.xlsx', sheet_name='19 decisions')
idx = {f: i for i, f in d.ft_id.items()}; log = []
def fq(ft, s):  # locate a quote tolerant to soft hyphens / line-break spacing; return verbatim text
    if not s: return ''
    t = T(ft)
    if s in t: return s
    pat = r'\s*'.join(re.escape(c).replace('\\-', '-.{0,2}') if c != ' ' else '' for c in s)
    pat = re.sub(r'(\\s\*)+', r'\\s*', pat); m = re.search(pat, t)
    return m.group(0) if m else None
ITEMS = ['A1','A2','B1','B2','B3','B4','B5','C1','C2','D1','E1','E2','F1','G1','X1','X2','X3','X4','X5','X6']
TYPE = {'FT065': 'T1', 'FT264': 'T2', 'FT215': 'T3', 'FT247': 'T3'}
NA = {'T1': [], 'T2': ['B3','B4','B5','C2','E2'], 'T3': ['A2','B2','B3','B4','B5','C1','C2','E1','E2','F1','X1','X2','X3','X4','X5','X6']}
# 1) four papers now included: codes from the GPT pass, every quote re-located verbatim in the full text
for ft, ty in TYPE.items():
    i = idx[ft]; old = d.at[i, 'ft_decision']; d.at[i, 'ft_decision'] = 'include'; d.at[i, 'study_type'] = ty; d.at[i, 'coder'] = 'GPT pass, verified + adjudicated'
    Q = g.loc[ft, 'quotes'] if isinstance(g.loc[ft, 'quotes'], dict) else {}
    for it in ITEMS:
        c = 'NA' if it in NA[ty] else g.loc[ft, it]
        parts = [Q.get(it, '')] + ([Q.get('G1_funding',''), Q.get('G1_conflict','')] if it == 'G1' else []) + ([Q.get('D1_destination','')] if it == 'D1' else [])
        vq = [fq(ft, p) for p in parts if p]
        if any(v is None for v in vq) and c in ('R', 'P'): print('UNVERIFIED', ft, it, parts)
        d.at[i, it] = c; d.at[i, it + '_q'] = ' || '.join(v for v in vq if v) if c not in ('NA','N') else ''
    d.at[i, 'R'] = 'none'; d.at[i, 'R_q'] = ''
    if ft == 'FT065': d.at[i,'X6'] = 'no'; d.at[i,'X1'] = 'Grounded/RAG'
    if ft == 'FT264': d.at[i,'X6'] = 'no'; d.at[i,'X1'] = 'Unclear'
    log.append(dict(ft_id=ft, item='inclusion', old=old, new=f'include {ty}', reason=A[A['FT ID']==ft]['Decision note'].iloc[0]))
# 2) B1 and X1 decisions
for _, r in A[A.Item.isin(['B1','X1'])].iterrows():
    ft, it, new = r['FT ID'], r['Item'], str(r['YOUR DECISION']).strip(); i = idx[ft]; old = d.at[i, it]
    ev = fq(ft, str(r['Paper evidence']).strip().rstrip('.'))
    if ev is None: print('EVIDENCE NOT FOUND', ft, it, r['Paper evidence'])
    if new != old:
        d.at[i, it] = new; d.at[i, it + '_q'] = ev or ''
    log.append(dict(ft_id=ft, item=it, old=old, new=new, reason=r['Decision note'], quote=ev))
d.to_pickle('coded_final.pkl'); L = pd.DataFrame(log); L.to_csv('adjudication_round2_log.csv', index=False)
print(L[['ft_id','item','old','new']].to_string(index=False))
# fixes after verification
i = idx['FT264']; d.at[i,'F1'] = 'N'; d.at[i,'F1_q'] = ''   # GPT's F1 quote (artist URL) is not in the text and is not a data statement
i = idx['FT301']; d.at[i,'B1_q'] = q('FT301', r"utilized the OpenAI GPT-4 Turbo API") + ' || ' + q('FT301', r"The ÈPizzul AI Assistant was launched and made accessible to the public on April 29, 2024")
i = idx['FT159']; d.at[i,'B1_q'] = d.at[i,'B1_q']
# spot-check (10 papers): GC 10/10 agree; MV 9/10 agree. FT002: MV -> N, X6 stays no via setup/tool-development caveat
X = pd.read_csv('x6_v12_three_judgments.csv'); X.loc[X.ft_id=='FT002',['model_version_caveat','setup_caveat']] = ['N','Y']
for ft, ty in [('FT065','T1'),('FT264','T2')]:
    X = pd.concat([X, pd.DataFrame([dict(ft_id=ft, type=ty, general_claim='N', model_version_caveat='N', setup_caveat='N', X6='no', X6_v11='', X6_quote='')])])
X.to_csv('x6_final.csv', index=False); d.to_pickle('coded_final.pkl'); print('saved')
