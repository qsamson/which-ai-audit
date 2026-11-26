import re,glob,pandas as pd,sys
d=pd.read_pickle('coded.pkl'); inc=d[(d.ft_decision=='include')&(d.B1=='P')].sort_values('ft_id')
def T(ft):
    p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    return re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
MON=r"(January|February|March|April|May|June|July|August|September|October|November|December|spring|summer|fall|autumn|winter|Spring|Summer|Fall|Autumn|Winter)"
DATE=MON+r",? (of )?(\d{1,2}(st|nd|rd|th)?,? )?20(2[2-6])|\b20(2[2-6])-\d\d-\d\d\b|\b\d{1,2}(st|nd|rd|th)? "+MON+r",? 20(2[2-6])"
CTX=r"(collect|conduct|queried|quer|prompt|generat|accessed|retriev|experiment|took place|tested|evaluat|deployed|version|interview|survey|recruit|between|from)"
BAD=r"Received|Accepted|Published|Revised|Downloaded|©|Copyright|Publication date|Article [A-Z]|pages\. https|Proc\. ACM|doi\.org|released|release of|launch|introduced|announced|et al"
VER=r"(GPT-?[345](\.5)?(-?o|-?turbo| Turbo)?(-mini)?|gpt-[\w.-]+|Claude[ -]\d[\w. -]{0,12}|Gemini[ -]\d[\w.]*|Llama[ -]?\d[\w.-]*|LLaMA[ -]?\d|Mistral[ -]\w+|DALL[·-]?E ?\d|Midjourney (v|V)\d|Stable Diffusion (XL|\d[\w.]*)|Bard|Copilot|ERNIE[ \w.]{0,6}|Qwen[\w.-]*|DeepSeek[- ]\w+)"
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for _,r in inc.iloc[lo:hi].iterrows():
    ft=r.ft_id; t=T(ft); n=len(t)
    refs=[m.start() for m in re.finditer(r"\bReferences\b|\bREFERENCES\b",t) if m.start()>n*0.5]; end=refs[-1] if refs else n
    c=[]
    for m in re.finditer(DATE,t[:end]):
        w=t[max(0,m.start()-140):m.end()+50]
        if re.search(CTX,w,re.I) and not re.search(BAD,w): c.append(w)
    v=sorted(set(x.group(0) for x in re.finditer(VER,t[:end])))
    print(f"## {ft} {r.study_type} | ver: {', '.join(v[:8])}")
    for x in c[:3]: print('   -',x)
