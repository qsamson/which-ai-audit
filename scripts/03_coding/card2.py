import json,sys,re,glob,pandas as pd
R=json.load(open('autocode.json'))
F=pd.read_excel('which_ai_master_screening.xlsx',sheet_name='Full-text list').set_index('ft_id')
def txt(ft):
    p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    return re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
for ft in sys.argv[1:]:
    r=R[ft]; f=F.loc[ft]; t=txt(ft); S=re.split(r"(?<=[.!?])\s+(?=[A-Z(\"“])",t); n=len(S)
    print(f"#### {ft} | {f.journal[:30]} | scr={f.decision} | {f.title[:100]}")
    if f.decision=='unclear': print("  scr-note:",str(f.ai_note)[:120])
    des=[s for i,s in enumerate(S) if n*0.08<i<n*0.6 and len(s)<400 and re.search(r"\b(participants?|respondents?|we (conducted|collected|recruited|interviewed|surveyed|analy[sz]ed|prompted|used|developed|designed|built|generated|queried))\b",s,re.I)][:3]
    for s in des: print("  D:",s[:260])
    print("  names:",", ".join(r['names'][:8]))
    for k,v in r['codes'].items():
        if v[0] not in ("N","none found"): print(f"  {k}:{v[0]} "+" || ".join(x[:150] for x in v[1:] if x))
