import re,pandas as pd,json
from mkq import T
d=pd.read_pickle('coded_v11.pkl'); s=d[(d.ft_decision=='include')&(d.study_type!='T3')].sort_values('ft_id')
GEN=r"\b(generative AI|GenAI|GAI|AI|LLMs?|large language models?|chatbots?|AI-generated|AIGC|conversational agents?|AI tools?|AI systems?|T2I|text-to-image)\b"
SPEC=r"(ChatGPT|GPT-?\d|Claude|Gemini|Llama|LLaMA|Midjourney|DALL|Stable Diffusion|SDXL|Copilot|Bard|Replika|Grok|Kimi|Doubao|our (system|tool|app|prototype|framework|chatbot|agent))"
VERB=r"(suggest|show|indicat|reveal|highlight|demonstrat|underscore|illustrat|find|found|conclud|implication|can |may |could )"
MV=r"(specific (type of )?(GenAI |AI |generative AI |language )?(model|LLM|version|tool|chatbot|platform)|single (model|LLM|AI tool|tool|platform|chatbot|generative)|only (one|two|three) (LLMs?|models?|chatbots?|tools?|platforms?)|(other|different|newer|future|later|alternative|more advanced|additional) (LLMs|models|model versions|versions|AI models|AI tools|chatbots|GenAI tools|generative AI (tools|models|systems)|T2I platforms|platforms|image generators)|version[- ]sensitiv|models? (are|is) (frequently|regularly|continuously|constantly)? ?updated|frequency at which models are updated|(rapid|ongoing) model evolution|(further|future) development of (GenAI|AI|generative AI|these) tools|at the time of (the |this |our )?(study|writing|data collection)|(constantly|continuously) (modify|update|evolv|chang)\w*|circumscribed to|exclusively (focused|relied) on (ChatGPT|GPT|the)|choice of [A-Z][\w ]{0,25} as the)"
SET=r"(prompt(s|ing)?|temperature|parameters?|configuration|system (prompt|instructions)|instructions (given|provided) to|persona|stimul(i|us)|interface|wizard|pre-?programmed|scripted|first (generated )?(response|output|draft)|single (draw|response|generation)|one first-pass)"
LIMH=r"(Limitations?|LIMITATIONS?|limitations of (this|our|the present) (study|work|research)|study has (several |some )?limitations|Future (research|work|directions))"
out={}
for _,r in s.iterrows():
    t=T(r.ft_id); n=len(t)
    refs=[m.start() for m in re.finditer(r"\bReferences\b|\bREFERENCES\b|\bBibliography\b",t) if m.start()>n*0.5]; end=refs[-1] if refs else n
    sents=lambda a,b: re.split(r"(?<=[.!?])\s+(?=[A-Z])",t[a:b])
    ci=[m.start() for m in re.finditer(r"\b(Conclusions?|CONCLUSIONS?|Concluding remarks)\b",t[:end]) if m.start()>n*.4]
    zone=sents(0,int(n*.07))+(sents(ci[0],min(end,ci[0]+3500)) if ci else sents(int(end*.82),end))
    gc=[x for x in zone if re.search(GEN,x) and re.search(VERB,x,re.I) and not re.search(SPEC,x) and 50<len(x)<330][:3]
    body=t[int(n*.35):end]
    mv=[]
    for m in re.finditer(MV,body,re.I):
        w=body[max(0,m.start()-170):m.end()+130]
        if re.search(r"limit|caveat|caution|generali|may (not|differ|vary|change)|might|future|should|depend|influence|affect|restrict|replicat",w,re.I) and not any(w[60:200] in x for x in mv): mv.append(w)
    li=[m.start() for m in re.finditer(LIMH,t[:end]) if m.start()>n*.4]
    st=[]
    for a in li[:2]:
        for x in sents(a,min(end,a+3500)):
            if re.search(SET,x,re.I) and len(x)<380 and x not in st: st.append(x)
    out[r.ft_id]=dict(type=r.study_type,x6=r.X6,x6q=r.X6_q,gc=gc,mv=mv[:3],st=st[:3],haslim=bool(li))
json.dump(out,open('ev3.json','w'))
print(len(out))
