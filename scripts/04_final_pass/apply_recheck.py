"""Final pass (codebook v1.1): apply re-check overrides on top of coded.pkl -> coded_v11.pkl. Verifies every quote."""
import re, pandas as pd
from mkq import T, q
from spec_b1 import S as B1
from spec_x6e1 import X6, E1, E2
d = pd.read_pickle('coded.pkl').copy(); log = []
inc = d.ft_decision == 'include'
def setq(i, item, code, quote, why):
    old = d.at[i, item]; d.at[i, item] = code; d.at[i, item+'_q'] = quote
    log.append(dict(ft_id=d.at[i,'ft_id'], item=item, old=old, new=code, reason=why, quote=quote))
idx = {f: i for i, f in d.ft_id.items()}
# 1 B1
for ft, (c, ps, n) in B1.items(): setq(idx[ft], 'B1', c, ' || '.join(q(ft, p) for p in ps), 'B1 re-check: ' + (n or 'version + date of use stated'))
# 2 G1
g = pd.read_pickle('reliability/g1_recheck.pkl').set_index('ft')
G1FIX = {'FT256': ('N', '', ''), 'FT210': ('R', r"The original data was collected by myself as part of an Horizon project \(EU Commission funded\)", None),
         'FT194': ('R', None, r"Competing interests The authors have no relevant financial or non-financial interests to disclose\."),
         'FT097': ('R', None, r"There is no potential conflict of interest in this study\.")}
def trim(w):  # drop the 40-char lead-in window, keep ~170 chars from the match
    return w[40:210].strip() if w else ''
for ft, r in g.iterrows():
    i = idx[ft]; code, fq, cq = r.new, trim(r.fund_q), trim(r.coi_q)
    if ft in G1FIX:
        code, pf, pc = G1FIX[ft]
        if pf is not None: fq = q(ft, pf) if pf else ''
        if pc is not None: cq = q(ft, pc) if pc else ''
    quote = ' || '.join(x for x in [fq, cq] if x)
    if code != d.at[i, 'G1'] or quote != d.at[i, 'G1_q']: setq(i, 'G1', code, quote, 'G1 re-check: R = funding AND COI statement; P = one')
# 3 T3: only A1 B1 D1 G1 apply
for i in d[inc & (d.study_type == 'T3')].index:
    for it in ['X1','X2','X3','X4','X5','X6']:
        if d.at[i, it] != 'NA': setq(i, it, 'NA', '', 'Codebook: for T3 only A1 B1 D1 G1 apply')
# 4 X6
for ft, (c, ps) in X6.items(): setq(idx[ft], 'X6', c, q(ft, ps[0]) if ps else '', 'X6 v1.1: class-level conclusion AND no model/version caveat => yes')
GEN = r"\b(generative AI|GenAI|GAI|AI|LLMs|large language models|chatbots|AI chatbots|AI-generated|AIGC|conversational agents)\b"
SPEC = r"(ChatGPT|GPT-?\d|Claude|Gemini|Llama|Midjourney|DALL|Stable Diffusion|Copilot|Bard|Replika|Grok|Kimi|Doubao)"
VERB = r"(findings|results|study|data|we) (suggest|show|indicate|reveal|highlight|demonstrat|underscore|illustrat|find|found)"
for i in d[inc & (d.X6 == 'yes')].index:
    if d.at[i, 'X6_q']: continue
    t = T(d.at[i, 'ft_id']); n = len(t); best = ''
    for part in (t[:int(n*.12)], t[int(n*.55):int(n*.92)]):
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", part):
            if 60 < len(s) < 320 and re.search(GEN, s) and re.search(VERB, s, re.I) and not re.search(SPEC, s): best = s; break
        if best: break
    d.at[i, 'X6_q'] = best
    log.append(dict(ft_id=d.at[i,'ft_id'], item='X6', old='yes', new='yes', reason='quote added (class-level conclusion)' if best else 'NO QUOTE FOUND', quote=best))
# 5 E1
for ft, (c, ps) in E1.items(): setq(idx[ft], 'E1', c, q(ft, ps[0]), 'E1 re-check: human validation of AI outputs reported')
for ft, (c, ps) in E2.items(): setq(idx[ft], 'E2', c, q(ft, ps[0]) if ps else '', 'Adjudication: no transformation of outputs described')
d['version_and_date'] = d.B1.map(lambda x: 'yes' if x == 'R' else 'no')
# verify every quote
errs = []
for i, r in d[inc].iterrows():
    t = T(r.ft_id)
    for c in [c for c in d.columns if c.endswith('_q') and c != 'ft_reason_quote']:
        for part in str(r[c] or '').split(' || '):
            if part and part not in t: errs.append((r.ft_id, c, part[:60]))
L = pd.DataFrame(log); L.to_csv('recheck_log_v11.csv', index=False); d.to_pickle('coded_v11.pkl')
print('changes:', len(L[L.old != L.new]), '| quote errors:', errs[:10], len(errs)); print(L[L.old != L.new].groupby('item').size().to_dict())
print('X6 yes without quote:', L[L.reason == 'NO QUOTE FOUND'].ft_id.tolist())
