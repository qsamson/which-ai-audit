import re,glob,pandas as pd
d=pd.read_pickle('coded.pkl'); import sys; ids=open('x6no_ids.txt').read().split(); inc=d[d.ft_id.isin(ids)]
SKIP={'FT018','FT076','FT095','FT178','FT202','FT285','FT288'}
def T(ft):
    p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    return re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
GEN=r"\b(generative AI|GenAI|GAI|AI|LLMs|large language models|chatbots|AI chatbots|AI-generated|AIGC|conversational agents|text-to-image (models|generators))\b"
SPEC=r"(ChatGPT|GPT-?\d|Claude|Gemini|Llama|Midjourney|DALL|Stable Diffusion|Copilot|Bard|Replika|Grok|Kimi|Doubao|Pi\b)"
CONC=r"(suggest|show|demonstrat|indicat|reveal|highlight|find|found|can |may |implications?|conclu)"
for _,r in inc.sort_values('ft_id').iterrows():
    if r.ft_id in SKIP: continue
    t=T(r.ft_id); n=len(t)
    sents=re.split(r"(?<=[.!?])\s+(?=[A-Z])",t[:int(n*0.12)])+re.split(r"(?<=[.!?])\s+(?=[A-Z])",t[int(n*0.55):int(n*0.9)])
    c=[s for s in sents if re.search(GEN,s) and re.search(CONC,s,re.I) and not re.search(SPEC,s) and 60<len(s)<350]
    m=sorted(set(re.findall(SPEC,t)),key=lambda x:-t.count(x))[:3]
    print(f"## {r.ft_id} {r.study_type} models={m}")
    for s in c[:2]: print('    -',s[:300])
