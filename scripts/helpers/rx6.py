import re,glob,pandas as pd,sys
d=pd.read_pickle('coded.pkl'); inc=d[(d.ft_decision=='include')]
def T(ft):
    p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    return re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
LIM=r"((other|different|alternative|various|multiple) (tools|AI tools|generative AI|LLMs|image generators|text-to-image|GenAI|conversational agents|large language)\w*|ChatGPT-specific|particular (model|tool|LLM|version|chatbot)| (one|a single|two) (LLM|model|AI|chatbot|tool|platform|generative)|single (LLM|model|AI (tool|system|model)|tool|platform|chatbot)|(other|different|alternative|newer|future|later|subsequent) (LLMs|models|versions|AI (tools|models|systems|chatbots)|chatbots|GenAI tools|generative AI (tools|models|platforms)|platforms|model versions|iterations)|specific (model|version|LLM|tool|AI (tool|model|system)|chatbot)|(model|version)[- ]specific|(rapid(ly)?|constant(ly)?|continuous(ly)?) (evolv|chang|updat|develop|advanc)\w*|(may|might|could) (not )?generali[sz]e to (other|all)|generali[sz]ab\w+ (to|of (our|the|these) findings to) (other|all)|(evolving|changing) nature of (AI|LLM|generative|the technology|these (tools|models))|models? (are|is) (frequently|regularly|continuously|constantly) updated|updates? to the model)"
mode=sys.argv[1]
sel=inc[(inc.X6=='yes')&(inc.study_type!='T3')] if mode=='yes' else inc[inc.X6=='no']
for _,r in sel.sort_values('ft_id').iterrows():
    t=T(r.ft_id); n=len(t)
    refs=[m.start() for m in re.finditer(r"\bReferences\b|\bREFERENCES\b",t) if m.start()>n*0.5]; end=refs[-1] if refs else n
    h=[]
    for m in re.finditer(LIM,t[:end],re.I):
        w=t[max(0,m.start()-130):m.end()+110]
        if re.search(r"limit|caveat|future (research|work|studies)|should|generali|caution|may not|might not|restrict",w,re.I): h.append(w)
    print(f"## {r.ft_id} {r.study_type} X1={r.X1} hits={len(h)} | X6q={str(r.X6_q)[:120]}")
    for x in h[:3]: print('    -',x)
