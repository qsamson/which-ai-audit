import re,glob,sys
def T(ft):
    p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    return re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
KEY=r"(model|version|LLM|GPT|ChatGPT|Claude|Gemini|Llama|tool|platform|chatbot|AI|prompt|stimul|generated|configur|interface|system|setting|parameter)"
for ft in sys.argv[1:]:
    t=T(ft); n=len(t)
    secs=[m.start() for m in re.finditer(r"(Limitations?|LIMITATIONS?|limitations of (this|our|the present) (study|work|research)|study has (several |some )?limitations)",t) if m.start()>n*0.3]
    out=[]
    for s in secs[:2]:
        seg=t[s:s+3000]
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z])",seg):
            if re.search(KEY,sent) and len(sent)<400 and sent not in out: out.append(sent)
    print('##',ft,'(no limitations section found)' if not secs else '')
    for x in out[:5]: print('    -',x[:260])
