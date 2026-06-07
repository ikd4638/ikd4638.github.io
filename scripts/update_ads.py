#!/usr/bin/env python3

# ADS updater for publications
import os
import json
import requests

# ============================================
# FOR LOCAL TESTING ONLY - Remove this section when deploying!
# Set your token here for testing, or use environment variable
# NEVER commit this token to version control!
# ============================================
# Option 1: Set token directly (temporary testing only)
TOKEN = "2fE6RJyX9FxKvOJJZRSM8h9nazkTkVLWny3E1Bnr"

# Option 2: Use environment variable (recommended for production)
#TOKEN = os.environ.get("ADS_API_TOKEN")

if not TOKEN:
    print("ERROR: ADS_API_TOKEN not found!")
    print("Set it as environment variable or directly in the script for testing")
    print("export ADS_API_TOKEN='your_token_here'")
    sys.exit(1)
# ============================================

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# Search query for all Dihingia papers
url = (
    "https://api.adsabs.harvard.edu/v1/search/query"
    "?q=author:%22Dihingia%22"
    "&fl=title,author,pubdate,bibcode,citation_count,doi"
    "&rows=200"
)

try:
    r = requests.get(url, headers=headers)
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from ADS: {e}")
    sys.exit(1)

docs = r.json()["response"]["docs"]

papers = []

total_citations = 0
first_author_count = 0
many_authors_count = 0  # Papers with >10 authors (not EHT-specific)

for p in docs:
    title = p.get("title", [""])[0] if p.get("title") else ""
    authors = p.get("author", [])
    citations = p.get("citation_count", 0)
    
    total_citations += citations
    
    # Check if Dihingia is first author
    is_first = (
        len(authors) > 0 and 
        "Dihingia" in authors[0]
    )
    
    if is_first:
        first_author_count += 1
    
    # Check if paper has many authors (>10)
    has_many_authors = len(authors) > 10
    
    if has_many_authors:
        many_authors_count += 1
    
    # Get DOI if available
    doi = p.get("doi", [""])[0] if p.get("doi") else ""
    url_link = f"https://doi.org/{doi}" if doi else f"https://ui.adsabs.harvard.edu/abs/{p.get('bibcode', '')}"
    
    paper_info = {
        "title": title,
        "authors": authors,
        "citations": citations,
        "bibcode": p.get("bibcode", ""),
        "doi": doi,
        "url": url_link,
        "date": p.get("pubdate", ""),
        "first_author": is_first,
        "many_authors": has_many_authors,  # New field for >10 authors
        "num_authors": len(authors)  # Also store the actual count
    }
    
    papers.append(paper_info)

# Sort papers by date (most recent first)
papers.sort(key=lambda x: x.get("date", ""), reverse=True)

# Calculate metrics
metrics = {
    "total_publications": len(papers),
    "first_author_publications": first_author_count,
    "papers_with_many_authors": many_authors_count,  # Papers with >10 authors
    "total_citations": total_citations,
    "last_updated": __import__('datetime').datetime.now().isoformat()
}

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save publications JSON
with open("data/publications.json", "w", encoding="utf-8") as f:
    json.dump(papers, f, indent=2, ensure_ascii=False)

# Save metrics JSON
with open("data/metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)

print(f"ADS update complete!")
print(f"  - Total papers: {len(papers)}")
print(f"  - First author papers: {first_author_count}")
print(f"  - Papers with >10 authors: {many_authors_count}")
print(f"  - Total citations: {total_citations}")
print(f"\nData saved to data/publications.json and data/metrics.json")
