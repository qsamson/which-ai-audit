"""Merge auto first-pass codes with reviewed decisions. Verify every quote is in the full text."""
import json, re, glob, importlib, sys, pandas as pd
sys.path.insert(0, 'scripts/03_coding')
R = json.load(open('autocode.json'))
CORE = ['A1','A2','B1','B2','B3','B4','B5','C1','C2','D1','E1','E2','F1','G1']
NA = {'T1': [], 'T2': ['B3','B4','B5','C2','E2'], 'T3': ['A2','B2','B3','B4','B5','C1','C2','E1','E2','F1']}
def text(ft):
    p = [x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    t = re.sub(r"-\n(?=[a-z])", "", open(p).read()); return re.sub(r"\s+", " ", t)
def build(mods):
    rows = []; errs = []
    for modname in mods:
        D = importlib.import_module(modname).D
        for ft, d in D.items():
            t = text(ft); auto = R[ft]['codes']; row = dict(ft_id=ft, coder='Claude (AI-assisted, reviewed)', batch=modname)
            row['ft_decision'] = d.get('dec', 'include'); row['study_type'] = d.get('type', '')
            if row['ft_decision'] != 'include':
                q = d.get('dec_q', ''); row['ft_reason_quote'] = q
                if q and q not in t: errs.append((ft, 'dec', q))
                rows.append(row); continue
            ov = d.get('ov', {})
            for it in CORE:
                if it in NA[row['study_type']]: row[it] = 'NA'; row[it+'_q'] = ''; continue
                if it in ov:
                    v = ov[it]; c, q = (v, '') if isinstance(v, str) else v
                    if q == '@' : q = ' || '.join(x for x in auto[it][1:] if x) if it in auto else ''
                else:
                    c = auto[it][0].replace('?', '') if it in auto else 'N'; q = ' || '.join(x for x in auto[it][1:] if x) if it in auto else ''
                row[it] = c; row[it+'_q'] = q
                for part in q.split(' || '):
                    if part and part not in t: errs.append((ft, it, part[:80]))
            for it in ['X1','X2','X3','X4','X5','X6']:
                v = d.get(it, 'NA'); c, q = (v, '') if isinstance(v, str) else v
                if it == 'X6' and q == '@': q = auto['X6lim'][1]
                row[it] = c; row[it+'_q'] = q
                if q and q not in t: errs.append((ft, it, q[:80]))
            v = d.get('R', None) or ('disclosed' if auto['R'][0] == 'disclosed' else 'none')
            row['R'] = v; row['R_q'] = d.get('R_q', auto['R'][1] if v != 'none' else '')
            if row['R_q'] and row['R_q'] not in t: errs.append((ft, 'R', row['R_q'][:80]))
            row['models'] = d.get('models', ', '.join(R[ft]['names'][:8]))
            row['version_and_date'] = 'yes' if row.get('B1') == 'R' else 'no'
            row['notes'] = d.get('note', '')
            rows.append(row)
    return pd.DataFrame(rows), errs
if __name__ == '__main__':
    df, errs = build(sys.argv[1:]); print(len(df), 'rows; quote errors:', errs)
    df.to_pickle('coded.pkl')
