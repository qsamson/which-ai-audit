import re,glob,sys
def T(ft):
    p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    return re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
MON=r"(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|June?|July?|Aug(ust)?|Sep(t|tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?|spring|summer|fall|autumn|winter)\.?"
PAT=[MON+r",? (of )?(\d{1,2}(st|nd|rd|th)?,? )?(to [A-Z]\w+ )?20(2[2-6])", r"\b\d{1,2}(st|nd|rd|th)? "+MON+r",? 20(2[2-6])",
 r"\b20(2[2-6])[-/]\d\d([-/]\d\d)?\b", r"-(0[1-9]|1[0-2])(\d\d)\b", r"\b(as of|accessed|at the time of)\b[^.]{0,60}", r"(gpt|claude|gemini)[\w.-]*-20\d\d-?\d\d-?\d\d"]
BAD=r"Received|Accepted|Published|Revised|Downloaded|©|Copyright|Publication date|Article [A-Z]|pages\. https|Proc\. ACM|doi\.org|liebertpub|For personal use"
for ft in sys.argv[1:]:
    t=T(ft); n=len(t)
    refs=[m.start() for m in re.finditer(r"\bReferences\b|\bREFERENCES\b|\bBibliography\b",t) if m.start()>n*0.5]; end=refs[-1] if refs else n
    seen=[];print('##',ft)
    for p in PAT:
        for m in re.finditer(p,t[:end],re.I if p.startswith(r"\b(as") or 'gpt' in p else 0):
            s=t[max(0,m.start()-150):m.end()+70]
            if re.search(BAD,s) or any(abs(m.start()-x)<120 for x in seen): continue
            seen.append(m.start()); print('   -',s)
