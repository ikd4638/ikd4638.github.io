# ADS updater placeholder using ADS_API_TOKEN secret
import os
import json
import requests

TOKEN = os.environ["ADS_API_TOKEN"]

headers = {
"Authorization": f"Bearer {TOKEN}"
}

url = (
"https://api.adsabs.harvard.edu/v1/search/query"
"?q=author:%22Dihingia%22"
"&fl=title,author,pubdate,bibcode,citation_count"
"&rows=200"
)

r = requests.get(url, headers=headers)

r.raise_for_status()

docs = r.json()["response"]["docs"]

papers = []

total_citations = 0
first_author = 0
eht_papers = 0

for p in docs:

```
title = p.get("title", [""])[0]
authors = p.get("author", [])

citations = p.get("citation_count", 0)

total_citations += citations

is_first = (
    len(authors) > 0 and
    "Dihingia" in authors[0]
)

if is_first:
    first_author += 1

is_eht = (
    "Event Horizon Telescope" in title
    or "EHT" in title
)

if is_eht:
    eht_papers += 1

papers.append({
    "title": title,
    "authors": authors,
    "citations": citations,
    "bibcode": p.get("bibcode", ""),
    "date": p.get("pubdate", ""),
    "first_author": is_first,
    "eht": is_eht
})
```

metrics = {
"total_publications": len(papers),
"first_author": first_author,
"eht_papers": eht_papers,
"citations": total_citations
}

os.makedirs("data", exist_ok=True)

with open("data/publications.json", "w") as f:
json.dump(papers, f, indent=2)

with open("data/metrics.json", "w") as f:
json.dump(metrics, f, indent=2)

print("ADS update complete")

