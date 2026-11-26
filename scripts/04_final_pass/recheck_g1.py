import re,glob,pandas as pd
d=pd.read_pickle('coded.pkl'); inc=d[d.ft_decision=='include']
def T(ft):
    p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    return re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
FUND_CS=r"(\bFunding\b(?! ?acquisi)(?! for )(?! and )(?=.{0,220}([Ff]und|[Gg]rant|[Ss]upport|financ|ﬁnanc|award|[Ss]cholarship|None|[Nn]o |Foundation|Ministry|Council))|FU ?N ?D ?I ?N ?G|Funding [Ii]nformation|Open Access funding)"
FUND_CI=r"(funded (by|through|under)|funding support|\bGrant from|(received|receipt of|declare[sd]?|provided|reports?|that) .{0,40}(ﬁ|fi)nancial support|(ﬁ|fi)nancial support (was|from|by|for (the|this) (research|study|work))|grant/award|grant (no|number|agreement)|under grant|(supported|sponsored) (in part |partly |partially )?by (the |a )?([A-Z][\w&\-’']+ ){0,6}(Foundation|Fund|Council|Ministry|Agency|Program|Programme|Institute|University|Office|Award|Scholarship|Science|Academy|Commission|Department|Center|Centre|NSF|NIH|Grant)|did not receive any specific grant|received no (specific |external )?(funding|grant|financial)|no (external )?funding|self-funded|not receive any funding)"
COI=r"(con(fl|ﬂ)icts? of interests?|competing ((fi|ﬁ)nancial |non-(fi|ﬁ)nancial )?interests? (exist|to (declare|disclose))|known competing|declare no competing|no competing|declaration of (competing )?interests?|declaration of con(fl|ﬂ)icting interests?|no interests to disclose|Disclosure [Ss]tatement(?=.{0,80}(interest|competing|con(fl|ﬂ)ict)))"
def hits(t,pats):
    out=[]
    for pat,fl in pats:
        for m in re.finditer(pat,t,fl):
            w=t[max(0,m.start()-40):m.end()+160]
            pre=t[max(0,m.start()-40):m.start()]
            if re.search(r"et al\.|\((19|20)\d\d\)",pre) or re.search(r"^\S*\s?(and|in|of) [A-Z][a-z]+, [A-Z]\.",w[40:]): continue
            out.append(w)
    return out
rows=[]
for ft in inc.ft_id:
    t=T(ft)
    f=hits(t,[(FUND_CS,0),(FUND_CI,re.I)]); c=hits(t,[(COI,re.I),(r"CO ?N ?FL ?I ?C ?T O ?F I ?N ?T",0)])
    code='R' if f and c else ('P' if f or c else 'N')
    rows.append((ft,inc.set_index('ft_id').loc[ft,'G1'],code,f[0] if f else '',c[0] if c else ''))
R=pd.DataFrame(rows,columns=['ft','old','new','fund_q','coi_q']); R.to_pickle('reliability/g1_recheck.pkl'); old=pd.read_pickle('reliability/g1_recheck_v1.pkl').set_index('ft'); 
for _,r in R.iterrows():
    if old.loc[r.ft,'new']!=r.new: print('CHANGED',r.ft,old.loc[r.ft,'new'],'->',r.new,'| F:',r.fund_q[:100],'| C:',r.coi_q[:80])
print(pd.crosstab(R.old,R.new)); print(R.new.value_counts().to_dict())
