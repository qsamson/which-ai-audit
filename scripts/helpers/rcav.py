import re,glob,sys
def T(ft):
    p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    return re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
CAV=r"(at the time of (the |this |our )?(study|writing|data collection|research|experiment)|(currently|as currently) (designed|available|trained)|(snapshot|temporal)|(models?|tools?|systems?|platforms?|versions?) (are|is|were) (being )?(constantly |frequently |continuously |regularly )?(updated|changing|evolving|improving)|(may|might|could|would) (differ|vary|change|yield different)|newer (models|versions)|(other|different|more advanced|future) (LLMs|models|versions|AI (models|tools|systems)|chatbots|tools|generative AI)|single (model|LLM|tool|platform)|one (model|LLM|tool|platform)\b|specific (model|LLM|tool|platform|version|chatbot)|model choice|choice of (model|LLM|tool))"
for ft in sys.argv[1:]:
    t=T(ft); n=len(t)
    refs=[m.start() for m in re.finditer(r"\bReferences\b|\bREFERENCES\b",t) if m.start()>n*0.5]; end=refs[-1] if refs else n
    h=[]
    for m in re.finditer(CAV,t[int(n*0.45):end],re.I):
        s=int(n*0.45)+m.start(); w=t[max(0,s-160):s+len(m.group(0))+120]
        if not any(abs(s-x[0])<200 for x in h): h.append((s,w))
    print('##',ft,len(h))
    for _,w in h[:4]: print('    -',w)
