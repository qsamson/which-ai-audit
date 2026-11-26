"""
Which AI? -- OpenAlex search for the cross-disciplinary audit
==============================================================

One script, three steps:

  python which_ai_search.py search    # find journals + download all records (all 15 journals in one run)
  python which_ai_search.py pilot     # draw the random pilot sample (default 20 per field to screen, aim to code 10)
  python which_ai_search.py sample    # after screening: draw the final sample (20 per journal) from included papers

No extra installs needed: uses only Python's standard library (Python 3.8+).

Outputs (in the folder ./which_ai_output/):
  journals_resolved.csv   which OpenAlex journal each name matched -- CHECK THIS FIRST
  records_all.csv         every record found, de-duplicated, with empty screening columns
  prisma_counts.csv       records per journal and field + search date and query (for the PRISMA box)
  search_log.txt          exact queries run, date, totals (paste into the Methods section)
  pilot_sample.csv        random pilot sample (pilot step)
  final_sample.csv        random final sample (sample step)
"""

import csv
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

# =====================================================================
# 1. SETTINGS -- edit these
# =====================================================================

# Free key from https://openalex.org (Settings -> API). You can also set an
# environment variable OPENALEX_API_KEY instead of typing it here.
API_KEY = os.environ.get("OPENALEX_API_KEY", "PASTE_YOUR_KEY_HERE")

# Your email (OpenAlex asks for it so they can contact you if something breaks)
EMAIL = "your.email@university.edu"

YEARS = "2023-2026"

# Search terms (title and abstract). OpenAlex reads OR between terms and
# treats text in double quotes as an exact phrase.
SEARCH_TERMS = [
    '"ChatGPT"',
    '"large language model"',
    '"large language models"',
    '"LLM"',
    '"generative AI"',
    '"generative artificial intelligence"',
    '"GPT-4"',
    '"Gemini"',
    '"Claude"',
    '"Copilot"',
    '"AI chatbot"',
    '"AI agent"',
    '"agentic"',
]

# Journals by field. Optional ISSN makes the match exact; leave "" to match by name.
# After the first run, open journals_resolved.csv and check every match.
JOURNALS = {
    "Social sciences": [
        ("AI & Society", ""),
        ("Big Data & Society", ""),
        ("Social Science Computer Review", ""),
        # ("Social Sciences", ""),   # MDPI, the conference journal -- swap in if you prefer
    ],
    "Education": [
        ("Computers & Education", ""),
        ("British Journal of Educational Technology", ""),
        ("Computers and Education: Artificial Intelligence", ""),
    ],
    "Health and psychology": [
        ("Computers in Human Behavior", ""),
        ("JMIR Mental Health", ""),
        ("Cyberpsychology, Behavior, and Social Networking", ""),
    ],
    "Communication and media": [
        ("New Media & Society", ""),
        ("Journal of Computer-Mediated Communication", ""),
        ("Digital Journalism", ""),
    ],
    "Human-computer interaction": [
        ("International Journal of Human-Computer Studies", ""),
        ("Proceedings of the ACM on Human-Computer Interaction", ""),
        ("International Journal of Human-Computer Interaction", ""),
    ],
}

PILOT_PER_FIELD = 20     # papers drawn per field to screen for the pilot (aim: 10 included per field)
FINAL_PER_JOURNAL = 20   # papers drawn per journal for the full audit
RANDOM_SEED = 2027       # report this number in the paper so the sample can be reproduced

OUT_DIR = "which_ai_output"

# =====================================================================
# 2. OpenAlex helpers
# =====================================================================

BASE = "https://api.openalex.org"


def call(endpoint, params, retries=5):
    """GET an OpenAlex endpoint and return parsed JSON, with polite retries."""
    params = dict(params)
    if API_KEY and API_KEY != "PASTE_YOUR_KEY_HERE":
        params["api_key"] = API_KEY
    if EMAIL:
        params["mailto"] = EMAIL
    query = urllib.parse.urlencode(params, safe=':|,()"')
    url = f"{BASE}/{endpoint}?{query}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"which-ai-audit ({EMAIL})"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                wait = 2 ** attempt
                print(f"   server busy ({e.code}), retrying in {wait}s...")
                time.sleep(wait)
                continue
            body = e.read().decode("utf-8", "ignore")[:300]
            sys.exit(f"\nOpenAlex error {e.code} for {url}\n{body}\n"
                     "Check your API key and that the query is valid.")
        except urllib.error.URLError as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"\nCould not reach OpenAlex: {e}. Check your internet connection.")


def resolve_journal(name, issn):
    """Return (source_id, display_name, issn_l, works_count) for a journal."""
    if issn:
        data = call("sources", {"filter": f"issn:{issn}", "per_page": 5})
    else:
        data = call("sources", {"search": name, "per_page": 5})
    results = data.get("results", [])
    if not results:
        return None
    # Prefer an exact (case-insensitive) title match among journals/conferences
    for r in results:
        if r.get("display_name", "").lower().replace("&", "and") == name.lower().replace("&", "and"):
            return r
    return results[0]


def abstract_text(inverted_index):
    """OpenAlex stores abstracts as an inverted index; rebuild the plain text."""
    if not inverted_index:
        return ""
    positions = []
    for word, idxs in inverted_index.items():
        for i in idxs:
            positions.append((i, word))
    return " ".join(w for _, w in sorted(positions))


def search_query():
    return "(" + " OR ".join(SEARCH_TERMS) + ")"


def fetch_journal_works(source_id):
    """Download all matching works for one journal using cursor paging."""
    flt = ",".join([
        f"primary_location.source.id:{source_id}",
        f"publication_year:{YEARS}",
        "type:article",
        f"title_and_abstract.search:{search_query()}",
    ])
    cursor, works = "*", []
    while cursor:
        data = call("works", {"filter": flt, "per_page": 100, "cursor": cursor})
        works.extend(data.get("results", []))
        cursor = data.get("meta", {}).get("next_cursor")
        if not data.get("results"):
            break
        time.sleep(0.2)
    return works, flt


# =====================================================================
# 3. Steps
# =====================================================================

SCREEN_COLS = ["screen_title_abstract", "exclusion_reason", "full_text_decision",
               "full_text_exclusion_reason", "screener", "notes"]


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:   # utf-8-sig opens cleanly in Excel
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def step_search():
    os.makedirs(OUT_DIR, exist_ok=True)
    today = date.today().isoformat()
    print(f"Searching OpenAlex on {today} for {YEARS}\n")

    resolved, records, counts, log = [], {}, [], []
    log.append(f"Search date: {today}")
    log.append(f"Database: OpenAlex (https://openalex.org)")
    log.append(f"Years: {YEARS}; document type: article")
    log.append(f"Title/abstract query: {search_query()}\n")

    for field, journals in JOURNALS.items():
        for name, issn in journals:
            src = resolve_journal(name, issn)
            if not src:
                print(f"!! No OpenAlex match for '{name}' -- add its ISSN in JOURNALS and rerun")
                resolved.append({"field": field, "searched_name": name, "matched_name": "NO MATCH"})
                continue
            sid = src["id"].rsplit("/", 1)[-1]
            matched = src.get("display_name", "")
            flag = "" if matched.lower().replace("&", "and") == name.lower().replace("&", "and") else "  <-- check this match"
            print(f"[{field}] {name} -> {matched} ({sid}){flag}")
            resolved.append({"field": field, "searched_name": name, "matched_name": matched,
                             "openalex_id": sid, "issn_l": src.get("issn_l", ""),
                             "type": src.get("type", ""), "total_works": src.get("works_count", "")})

            works, flt = fetch_journal_works(sid)
            new = 0
            for wk in works:
                key = (wk.get("doi") or wk["id"]).lower()
                if key in records:
                    continue
                new += 1
                records[key] = {
                    "openalex_id": wk["id"].rsplit("/", 1)[-1],
                    "doi": wk.get("doi") or "",
                    "title": (wk.get("title") or "").replace("\n", " "),
                    "year": wk.get("publication_year", ""),
                    "journal": matched,
                    "field": field,
                    "authors": "; ".join(a.get("author", {}).get("display_name", "")
                                         for a in wk.get("authorships", [])[:10]),
                    "abstract": abstract_text(wk.get("abstract_inverted_index")),
                    "cited_by": wk.get("cited_by_count", ""),
                    "open_access_url": (wk.get("open_access") or {}).get("oa_url") or "",
                    "landing_page": (wk.get("primary_location") or {}).get("landing_page_url") or "",
                    **{c: "" for c in SCREEN_COLS},
                }
            dupes = len(works) - new
            counts.append({"field": field, "journal": matched, "openalex_id": sid,
                           "records_found": len(works), "duplicates_removed": dupes,
                           "records_kept": new, "search_date": today})
            log.append(f"{field} | {matched} ({sid}): {len(works)} found, {dupes} duplicates")
            print(f"     {len(works)} records found")

    rows = sorted(records.values(), key=lambda r: (r["field"], r["journal"], str(r["year"])))
    fields = list(rows[0].keys()) if rows else ["title"]
    write_csv(os.path.join(OUT_DIR, "records_all.csv"), rows, fields)
    write_csv(os.path.join(OUT_DIR, "journals_resolved.csv"), resolved,
              ["field", "searched_name", "matched_name", "openalex_id", "issn_l", "type", "total_works"])
    write_csv(os.path.join(OUT_DIR, "prisma_counts.csv"), counts,
              ["field", "journal", "openalex_id", "records_found", "duplicates_removed", "records_kept", "search_date"])

    total_found = sum(c["records_found"] for c in counts)
    log.append(f"\nTOTAL identified: {total_found}; after de-duplication: {len(rows)}")
    with open(os.path.join(OUT_DIR, "search_log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log))

    print(f"\nDone. {total_found} records identified, {len(rows)} after removing duplicates.")
    print(f"Files saved in ./{OUT_DIR}/  -- open journals_resolved.csv first and check every match.")


def step_pilot():
    path = os.path.join(OUT_DIR, "records_all.csv")
    if not os.path.exists(path):
        sys.exit("Run the search step first: python which_ai_search.py search")
    rows = read_csv(path)
    rng = random.Random(RANDOM_SEED)
    sample = []
    for field in JOURNALS:
        pool = [r for r in rows if r["field"] == field]
        picked = rng.sample(pool, min(PILOT_PER_FIELD, len(pool)))
        for i, r in enumerate(picked, 1):
            r["pilot_order"] = i      # screen in this order; stop once 10 are included
        sample.extend(picked)
        print(f"{field}: {len(picked)} drawn from {len(pool)}")
    fields = ["pilot_order"] + [k for k in rows[0].keys()]
    write_csv(os.path.join(OUT_DIR, "pilot_sample.csv"), sample, fields)
    print(f"\nSaved pilot_sample.csv (seed {RANDOM_SEED}). Screen in pilot_order; "
          "code the first 10 included papers per field.")


def step_sample():
    path = os.path.join(OUT_DIR, "records_all.csv")
    rows = read_csv(path)
    included = [r for r in rows if r.get("full_text_decision", "").strip().lower() in ("include", "included", "yes")]
    if not included:
        sys.exit("No papers marked 'include' in the full_text_decision column of records_all.csv yet.\n"
                 "Finish screening first (write 'include' for eligible papers), then rerun.")
    rng = random.Random(RANDOM_SEED)
    sample, report = [], []
    journals = sorted({r["journal"] for r in included})
    for j in journals:
        pool = [r for r in included if r["journal"] == j]
        picked = rng.sample(pool, min(FINAL_PER_JOURNAL, len(pool)))
        sample.extend(picked)
        report.append(f"{j}: {len(picked)} sampled of {len(pool)} eligible")
        print(report[-1])
    write_csv(os.path.join(OUT_DIR, "final_sample.csv"), sample, list(rows[0].keys()))
    print(f"\nSaved final_sample.csv: {len(sample)} papers (seed {RANDOM_SEED}). "
          f"Not sampled: {len(included) - len(sample)} (for the PRISMA box).")


if __name__ == "__main__":
    steps = {"search": step_search, "pilot": step_pilot, "sample": step_sample}
    if len(sys.argv) != 2 or sys.argv[1] not in steps:
        print(__doc__)
        sys.exit(1)
    steps[sys.argv[1]]()
