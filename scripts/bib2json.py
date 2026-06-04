import json
import re

with open("data/All-publications.bib", "r", encoding="utf-8") as f:
    text = f.read()

# Split on BibTeX entries
entries = re.split(r'@\w+\{', text)[1:]

papers = []

for entry in entries:

    title = ""
    journal = ""
    year = ""
    authors = []

    m = re.search(r'title\s*=\s*\{(.*?)\}', entry, re.S)
    if m:
        title = " ".join(m.group(1).replace("\n", " ").split())

    m = re.search(r'journal\s*=\s*\{(.*?)\}', entry, re.S)
    if m:
        journal = m.group(1).strip()

    m = re.search(r'year\s*=\s*([0-9]{4})', entry)
    if m:
        year = m.group(1)

    m = re.search(r'author\s*=\s*\{(.*?)\},', entry, re.S)
    if m:
        authors = [a.strip() for a in m.group(1).split(" and ")]

    papers.append({
        "title": title,
        "authors": authors,
        "year": year,
        "journal": journal,
        "first_author": (
            len(authors) > 0 and "Dihingia" in authors[0]
        ),
        "many_authors": (
            len(authors) > 10
        )
    })

papers.sort(key=lambda p: str(p["year"]), reverse=True)

with open("data/publications.json", "w", encoding="utf-8") as f:
    json.dump(papers, f, indent=2, ensure_ascii=False)

metrics = {
    "total_publications": len(papers),
    "first_author": sum(p["first_author"] for p in papers),
    "many_authors": sum(p["many_authors"] for p in papers)
}

with open("data/metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

print(f"Processed {len(papers)} papers")
