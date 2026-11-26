# Which AI? Find free preprint / author copies of the paywalled papers (single Colab cell)
# 1) Upload which_ai_pdf_checklist_v3.xlsx to Colab.  2) Run.  3) Upload the zip it downloads.
import os, re, time, json, zipfile, urllib.request, urllib.parse
import pandas as pd
EMAIL = "your.email@university.edu"
OUT = "preprints"; os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36", "Accept": "application/pdf,*/*"}
def get(url, js=True):
    req = urllib.request.Request(url, headers={"User-Agent": f"which-ai-audit (mailto:{EMAIL})"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r) if js else r.read()
def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower())
def same(a, b):
    a, b = set(norm(a).split()), set(norm(b).split())
    return len(a & b) / max(1, len(a)) > 0.8
def candidates(title, doi):
    urls = []
    d = str(doi).replace("https://doi.org/", "")
    try:  # Semantic Scholar: open-access PDF and arXiv id
        s = get(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(d)}?fields=title,openAccessPdf,externalIds")
        if s.get("openAccessPdf") and s["openAccessPdf"].get("url"): urls.append(("SemanticScholar", s["openAccessPdf"]["url"]))
        ax = (s.get("externalIds") or {}).get("ArXiv")
        if ax: urls.append(("arXiv", f"https://arxiv.org/pdf/{ax}"))
    except Exception: pass
    time.sleep(1.1)
    try:  # arXiv title search
        q = urllib.parse.quote(f'ti:"{title[:120]}"')
        x = get(f"http://export.arxiv.org/api/query?search_query={q}&max_results=3", js=False).decode()
        for e in re.findall(r"<entry>(.*?)</entry>", x, re.S):
            t = re.search(r"<title>(.*?)</title>", e, re.S).group(1); i = re.search(r"arxiv.org/abs/([^<]+)</id>", e).group(1)
            if same(title, t): urls.append(("arXiv", f"https://arxiv.org/pdf/{i}"))
    except Exception: pass
    try:  # OpenAlex: any repository location (accepted manuscripts)
        w = get(f"https://api.openalex.org/works/doi:{d}?mailto={EMAIL}")
        for l in w.get("locations") or []:
            if l.get("pdf_url"): urls.append(("OpenAlex-" + str((l.get("source") or {}).get("display_name")), l["pdf_url"]))
    except Exception: pass
    return urls
xl = pd.ExcelFile("which_ai_pdf_checklist_v3.xlsx")
df = pd.concat([pd.read_excel(xl, s) for s in xl.sheet_names if s.startswith(("Free", "Library"))])
log = []
for i, r in enumerate(df.itertuples(), 1):
    status, note = "NOT FOUND", ""
    for src, u in candidates(r.title, r.doi):
        try:
            data = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
            if data[:4] == b"%PDF":
                open(os.path.join(OUT, f"{r.ft_id}.pdf"), "wb").write(data); status, note = "FOUND", f"{src}: {u}"; break
        except Exception as e: note = f"{type(e).__name__} {src}"
        time.sleep(1)
    log.append([r.ft_id, r.journal, status, note]); print(f"{i}/{len(df)} {r.ft_id} {status} {note[:60]}")
L = pd.DataFrame(log, columns=["ft_id", "journal", "status", "source"]); L.to_csv(os.path.join(OUT, "preprint_log.csv"), index=False)
print(L.status.value_counts())
with zipfile.ZipFile("which_ai_preprints.zip", "w") as z:
    for f in os.listdir(OUT): z.write(os.path.join(OUT, f), f)
from google.colab import files; files.download("which_ai_preprints.zip")
