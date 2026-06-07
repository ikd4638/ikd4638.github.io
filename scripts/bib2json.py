#!/usr/bin/env python3

import json
import sys

try:
    import bibtexparser
except ImportError:
    print("Please install bibtexparser:")
    print("pip install bibtexparser")
    sys.exit(1)

# Check bibtexparser version and import appropriate functions
try:
    from bibtexparser import parse_string
    USE_NEW_API = True
except ImportError:
    USE_NEW_API = False

# Use raw strings (r"") to avoid escape sequence warnings
JOURNALS = {
    r"\apj": "The Astrophysical Journal",
    r"\apjl": "The Astrophysical Journal Letters",
    r"\apjs": "The Astrophysical Journal Supplement Series",
    r"\aj": "The Astronomical Journal",
    r"\mnras": "Monthly Notices of the Royal Astronomical Society",
    r"\aap": "Astronomy & Astrophysics",
    r"\nat": "Nature",
    r"\sci": "Science",
}

def clean_text(text):
    if not text:
        return ""

    text = text.replace("{", "")
    text = text.replace("}", "")

    return " ".join(text.split())

def clean_author(author):
    return clean_text(author)

def journal_name(journal):
    journal = clean_text(journal)

    if journal in JOURNALS:
        return JOURNALS[journal]

    return journal

def is_first_author(authors):
    if len(authors) == 0:
        return False

    return "dihingia" in authors[0].lower()

def display_authors(authors):
    authors = [clean_author(a) for a in authors]

    if len(authors) <= 3:
        return ", ".join(authors)

    return ", ".join(authors[:3]) + " et al."

def load_bib_file(bibfile):
    """Load bib file using the appropriate API for the installed version"""
    
    with open(bibfile, "r", encoding="utf-8") as f:
        bib_content = f.read()
    
    if USE_NEW_API:
        # For newer versions (1.4.0+)
        return parse_string(bib_content)
    else:
        # For older versions (pre-1.4.0)
        return bibtexparser.loads(bib_content)

def main():
    bibfile = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "data/All-publications.bib"
    )

    outfile = (
        sys.argv[2]
        if len(sys.argv) > 2
        else "data/publications.json"
    )

    # Load the bib file using the appropriate method
    bib_database = load_bib_file(bibfile)

    papers = []

    for entry in bib_database.entries:
        authors = []

        if "author" in entry:
            authors = [
                a.strip()
                for a in entry["author"].split(" and ")
            ]

        url = entry.get("adsurl", "")

        if not url:
            doi = entry.get("doi", "")
            if doi:
                url = "https://doi.org/" + doi

        paper = {
            "title": clean_text(entry.get("title", "")),
            "url": url,
            "authors": [clean_author(a) for a in authors],
            "display_authors": display_authors(authors),
            "year": str(entry.get("year", "")),
            "journal": journal_name(
                entry.get("journal", "")
            ),
            "volume": clean_text(
                entry.get("volume", "")
            ),
            "pages": clean_text(
                entry.get(
                    "pages",
                    entry.get("eid", "")
                )
            ),
            "first_author": is_first_author(authors),
            "many_authors": len(authors) > 10,
        }

        papers.append(paper)

    papers.sort(
        key=lambda p: p["year"],
        reverse=True
    )

    # Ensure the output directory exists
    import os
    os.makedirs(os.path.dirname(outfile) or ".", exist_ok=True)

    with open(
        outfile,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            papers,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Processed {len(papers)} papers"
    )
    print(
        f"Written to {outfile}"
    )

if __name__ == "__main__":
    main()
