# Which AI? Full-text PDF downloader (single Colab cell)
# 1) Upload which_ai_master_screening.xlsx to Colab (Files panel, left)
# 2) Run this cell. It downloads every open-access PDF it can, names it FTxxx_Wxxxx.pdf,
#    writes download_log.csv (what failed and why), and zips everything for download.
import os, time, json, zipfile, urllib.request, urllib.parse
import pandas as pd

EMAIL = "your.email@university.edu"   # used by Unpaywall and OpenAlex polite pool
ONLY_FREE = True                         # False = also try the "library / request" papers
OUT = "fulltexts"
os.makedirs(OUT, exist_ok=True)

KEY = None
try:
    from google.colab import userdata
    for k in ["OPENALEX","OPENALEX_KEY","OPENALEX_API_KEY","OPENALEX_API"]:
        try:
            KEY = userdata.get(k)
            if KEY: break
        except Exception:
            pass
except Exception:
    pass

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept": "application/pdf,*/*"}

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"which-ai-audit (mailto:{EMAIL})"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def candidate_urls(oid, doi):
    urls = []
    try:
        q = f"https://api.openalex.org/works/{oid}?mailto={EMAIL}" + (f"&api_key={KEY}" if KEY else "")
        w = get_json(q)
        locs = ([w.get("best_oa_location")] if w.get("best_oa_location") else []) + (w.get("locations") or [])
        for l in locs:
            if l and l.get("pdf_url"): urls.append(l["pdf_url"])
        for l in locs:
            if l and l.get("is_oa") and l.get("landing_page_url"): urls.append(l["landing_page_url"])
    except Exception:
        pass
    if isinstance(doi, str) and doi:
        d = doi.replace("https://doi.org/", "")
        try:
            u = get_json(f"https://api.unpaywall.org/v2/{urllib.parse.quote(d)}?email={EMAIL}")
            for l in ([u.get("best_oa_location")] if u.get("best_oa_location") else []) + (u.get("oa_locations") or []):
                if l and l.get("url_for_pdf"): urls.append(l["url_for_pdf"])
        except Exception:
            pass
    seen, out = set(), []
    for u in urls:
        if u not in seen: seen.add(u); out.append(u)
    return out

def try_download(url, path):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if data[:4] == b"%PDF":
        open(path, "wb").write(data); return True, len(data)
    return False, "not a PDF (landing page or blocked)"

df = pd.read_excel("which_ai_master_screening.xlsx", sheet_name="Full-text list")
if ONLY_FREE:
    df = df[df.access.str.startswith("free")]
log = []
for i, r in enumerate(df.itertuples(), 1):
    name = f"{r.ft_id}_{r.oid}.pdf"; path = os.path.join(OUT, name)
    if os.path.exists(path):
        log.append([r.ft_id, r.oid, "already have", ""]); continue
    status, note = "FAILED", "no open-access PDF link found"
    for u in candidate_urls(r.oid, r.doi):
        try:
            ok, info = try_download(u, path)
            if ok: status, note = "OK", u; break
            note = f"{info}: {u}"
        except Exception as e:
            note = f"{type(e).__name__}: {u}"
        time.sleep(1)
    log.append([r.ft_id, r.oid, status, note])
    print(f"{i}/{len(df)} {r.ft_id} {status}")
    time.sleep(1)

L = pd.DataFrame(log, columns=["ft_id", "oid", "status", "note"])
L.to_csv(os.path.join(OUT, "download_log.csv"), index=False)
print(L.status.value_counts())
with zipfile.ZipFile("which_ai_fulltexts.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir(OUT): z.write(os.path.join(OUT, f), f)
from google.colab import files
files.download("which_ai_fulltexts.zip")
