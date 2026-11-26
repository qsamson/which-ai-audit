import re,glob,pandas as pd
d=pd.read_pickle('coded.pkl'); inc=d[(d.ft_decision=='include')&(d.B1=='P')]
def T(ft):
    p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    return re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
MON=r"(January|February|March|April|May|June|July|August|September|October|November|December|Jan\.|Feb\.|Mar\.|Apr\.|Jun\.|Jul\.|Aug\.|Sept?\.|Oct\.|Nov\.|Dec\.|spring|summer|fall|autumn|winter|Spring|Summer|Fall|Autumn|Winter)"
DATE=MON+r",? (of )?(\d{1,2}(st|nd|rd|th)?,? )?20(2[2-6])|\b20(2[2-6])-\d\d-\d\d\b|\b\d{1,2}[./]\d{1,2}[./](20)?2[2-6]\b"
CTX=r"(collect|conduct|queried|prompt|generat|accessed|retriev|ran |run |experiment|study (was|took)|data|interact|took place|used|tested|evaluat|deployed|version)"
rows=[]
for ft in inc.ft_id:
    t=T(ft); n=len(t)
    refs=[m.start() for m in re.finditer(r"\bReferences\b|\bREFERENCES\b",t) if m.start()>n*0.5]; end=refs[-1] if refs else n
    c=[]
    for m in re.finditer(DATE,t[:end]):
        w=t[max(0,m.start()-170):m.end()+60]
        if re.search(CTX,w,re.I) and not re.search(r"Received|Accepted|Published|Revised|Downloaded|©|Copyright|et al|\(\d{4}[a-z]?\)",w): c.append(w)
    rows.append((ft,c[:3]))
for ft,c in rows:
    if c: print('##',ft); [print('  ',x) for x in c]
print(sum(1 for _,c in rows if c),'of',len(rows),'B1=P papers have a candidate date')
