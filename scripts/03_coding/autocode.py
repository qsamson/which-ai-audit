"""Rule-based first pass for GUIDE-LLM reporting items. Every quote is an exact substring of the cleaned full text.
A human (Claude + co-author) reviews each card and sets the judgment items (study type, A1, A2, X1-X6)."""
import re, glob, json, sys, pandas as pd
M = r"(ChatGPT|GPT-?\s?[2-5](\.\d)?[o]?(-turbo|-mini|o)?|gpt-[\w.-]+|GPT-?4o|Llama[\s-]?\d?|LLaMA|Gemini|Bard|Claude|Mistral|Mixtral|Copilot|Replika|DALL[·\-]?E ?\d?|Midjourney|Stable Diffusion|Sora|ERNIE|Qwen|DeepSeek|Character\.ai|Perplexity|Pi\b|Bing Chat|Doubao|Kimi|Xiaoice|Snapchat My AI|Grok|Phi-\d|Falcon|BERT|Whisper)"
VER = r"(GPT-?\s?(3\.5|4|4o|4\.1|4\.5|5)[\w.-]*|gpt-[\w.-]*\d|o1|o3|Llama[\s-]?\d(\.\d)?|Claude[\s-]?\d|Claude (3|3\.5|3\.7|4) (Opus|Sonnet|Haiku)|Gemini[\s-]?\d(\.\d)?|version \d[\w.]*|v\d\.\d|Midjourney (Version |v)?\d|DALL[·\-]?E ?[23]|Stable Diffusion (XL|\d)|\b\d{4}-\d\d-\d\d\b|-\d{4}\b)"
DATE = r"((January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?,? (\d{1,2}(st|nd|rd|th)?,? )?20(2[2-6]))|\b\d{1,2}[./]\d{1,2}[./](20)?2[2-6]\b|accessed|retrieved on|knowledge cutoff"
P = {
 'B2': r"\bAPI\b|application programming interface|web (interface|version|browser)|chat interface|ChatGPT (website|interface|app)|via the (OpenAI|ChatGPT) (platform|website)|Playground|Hugging ?Face|run locally|locally (hosted|deployed)|Azure OpenAI",
 'B3': r"temperature|top[-_ ]?p\b|max(imum)?[-_ ]tokens|\bseed\b|default (settings|parameters|hyper-?parameters)|frequency penalty|presence penalty",
 'B4': r"fine-?tun|custom(ized|ised)? (GPT|assistant|model|chatbot|instructions)|GPTs\b|GPT Builder|retrieval[- ]augmented|\bRAG\b|knowledge base|vector (database|store)|LoRA|trained on our",
 'B5': r"\bmemory\b|conversation history|chat history|context window|previous (conversation|session)s?|new (chat|session|conversation) for each|cleared",
 'C1': r"(full|complete|exact|following|verbatim) prompts?|prompts? (is|are|was|were) (provided|shown|listed|presented|reported|available|included)|prompts? in (the )?(appendix|supplement|table)|(appendix|supplement\w*|table) \w* ?(lists|shows|contains|presents|provides) (the )?(full |complete )?prompt|prompt template|prompt:",
 'C1p': r"\bprompt(s|ed|ing)?\b",
 'C2': r"system (prompt|message|instruction|role)|custom instructions|role prompt|pre-?prompt|persona (prompt|instruction)",
 'D1': r"(anonymi[sz]|de-?identif|personal(ly)? (data|information|identifiable)|privacy|confidential|sensitive (data|information))",
 'D1ai': r"(GPT|LLM|language model|OpenAI|API|ChatGPT|AI tool|chatbot|model|uploaded|entered|input|fed)",
 'E1': r"(manual(ly)?|human|research(er|ers)|author(s)?|expert(s)?|two coders|annotator(s)?) (\w+ ){0,3}(check|verif|review|validat|inspect|evaluat|cod|rat|assess)\w*|inter-?rater|intercoder|Cohen'?s kappa|Krippendorff|hallucinat\w* (were|was) (checked|identified|removed)",
 'E1ai': r"(output|response|generated|answer|text|image|completion|transcript|summar)",
 'E2': r"post-?process|clean(ed|ing) (the )?(output|response|generated)|(edited|removed|filtered|excluded|discarded|normali[sz]ed) (\w+ ){0,3}(output|response|generated|image|answer)",
 'F1': r"github\.com|osf\.io|zenodo|figshare|dataverse|huggingface\.co|code (and data )?(is|are) (publicly )?available|available (up)?on (reasonable )?request|data availability|supplementa(l|ry) (material|data|information|file)",
 'Gf': r"(?<!Funding )(?<!, )(this|the) (work|research|study|project|article) (was|is) (supported|funded|financed)|funded by|funding (from|was|for|:)|\bfunding\b|grant (no|number|agreement)|financial support|no (specific )?(funding|grant)",
 'Gc': r"conflicts? of interest|competing (financial )?interests?|disclosure statement|declaration of (interest|competing)",
 'R': r"(used|use of|using|assisted by|with the (help|assistance) of) (\w+ ){0,3}(ChatGPT|GPT|Grammarly|DeepL|Gemini|Claude|Copilot|generative AI|AI[- ]assisted|AI tool|language model|LLM)\w* (to|for|in) (\w+ ){0,4}(edit|proofread|language|grammar|readab|translat|polish|writing|copy)|declaration of generative AI|generative AI (and AI-assisted technologies )?in the writing|AI disclosure statement|use of AI (tools|technologies) statement",
}
def clean(t):
    t = re.sub(r"-\n(?=[a-z])", "", t); return re.sub(r"\s+", " ", t)
def sentences(t):
    return re.split(r"(?<=[.!?])\s+(?=[A-Z(\"“\[])", t)
def code(ft):
    p = [x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    t = clean(open(p).read()); S = sentences(t); n = len(S)
    refs = [i for i, s in enumerate(S) if re.search(r"\bReferences\b|\bREFERENCES\b|\bBibliography\b", s) and i > n * 0.5]
    rs = refs[0] if refs else n
    body = [(i, s) for i, s in enumerate(S) if i < rs and len(s) < 900]
    meth = [(i, s) for i, s in body if i > n * 0.12]
    tail = [(i, s) for i, s in enumerate(S) if len(s) < 900 and (i > n * 0.55)]
    def find(pat, pool, extra=None, k=1):
        rx = re.compile(pat, re.I); ex = re.compile(extra, re.I) if extra else None
        h = [s for i, s in pool if rx.search(s) and (ex is None or ex.search(s))]
        return h[:k]
    C = {}
    # B1
    named = find(M, meth, k=50); ver = [s for s in named if re.search(VER, s)]; dated = [s for i, s in body if re.search(DATE, s) and re.search(M + "|model|tool|chatbot|data (were )?collected", s, re.I) and 'Downloaded from' not in s and 'downloaded from' not in s]
    names = sorted({m.group(0).strip() for s in named for m in re.finditer(M, s)}, key=str.lower)
    if ver and dated: C['B1'] = ('R?', ver[0], dated[0])
    elif ver: C['B1'] = ('P', ver[0], '')
    elif named: C['B1'] = ('P', named[0], '')
    else: C['B1'] = ('N', '', '')
    for it in ['B2', 'B3', 'B4', 'B5', 'C2', 'E2']:
        h = find(P[it], meth); C[it] = ('R?' if h else 'N', h[0] if h else '', '')
    h = find(P['C1'], meth)
    if h: C['C1'] = ('R?', h[0], '')
    else:
        h = [s for i, s in meth if re.search(P['C1p'], s, re.I) and re.search(r"[\"“].{15,}[\"”]", s)]
        C['C1'] = ('P?' if h else 'N', h[0] if h else '', '')
    h = find(P['D1'], meth, P['D1ai']); C['D1'] = ('R?' if h else 'N', h[0] if h else '', '')
    if not h:
        h = find(r"ethic(s|al) (approval|committee|review|board)|\bIRB\b|institutional review|informed consent", body)
        if h: C['D1'] = ('P?', h[0], '')
    h = find(P['E1'], meth, P['E1ai']); C['E1'] = ('R?' if h else 'N', h[0] if h else '', '')
    h = find(P['F1'], body + tail); C['F1'] = ('R?' if h and re.search(r"github|osf|zenodo|figshare|dataverse|huggingface", h[0], re.I) else ('P?' if h else 'N'), h[0] if h else '', '')
    gf = [x for x in find(P['Gf'], tail, k=5) if not re.search(r'Funding acquisition', x)][:1]; gc = find(P['Gc'], tail)
    C['G1'] = ('R' if gf and gc else ('P' if gf or gc else 'N'), gf[0] if gf else '', gc[0] if gc else '')
    lim = [x for i, x in body if i > n*0.5 and re.search(r"limitation|caution|generaliz|generalis", x, re.I) and re.search(r"(specific|particular|single|one|other|different|newer|future|updated?) (\w+ ){0,2}(model|version|tool|chatbot|LLM|system|platform)s?|version|model updates|"+M, x, re.I)]
    C['X6lim'] = ('model-limit found' if lim else 'none found', lim[0] if lim else '', '')
    h = find(P['R'], body + tail); C['R'] = ('disclosed' if h else 'none found', h[0] if h else '', '')
    for k, v in C.items():
        for q in v[1:]:
            assert q == '' or q in t, (ft, k)
    return dict(ft=ft, words=len(t.split()), names=names, codes=C)
if __name__ == "__main__":
    ids = sorted({x.split('/')[-1][:5] for x in glob.glob('ft_txt/FT*.txt')})
    res = {ft: code(ft) for ft in ids}
    json.dump(res, open('autocode.json', 'w'), indent=0)
    print(len(res), 'coded')
    df = pd.DataFrame({ft: {k: v[0] for k, v in r['codes'].items()} for ft, r in res.items()}).T
    for c in df.columns: print(c, df[c].value_counts().to_dict())
