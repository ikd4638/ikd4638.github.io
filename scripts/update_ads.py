#!/usr/bin/env python3

# ADS updater for publications
import os
import json
import requests
import sys
from datetime import datetime

# ============================================
# FOR LOCAL TESTING ONLY - Remove this section when deploying!
# NEVER commit this token to version control!
# ============================================
TOKEN = os.environ.get("ADS_API_TOKEN")

if not TOKEN:
    print("ERROR: ADS_API_TOKEN not found!")
    print("Set it as environment variable: export ADS_API_TOKEN='your_token_here'")
    sys.exit(1)
# ============================================

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

def clean_text(text):
    """Clean text by removing extra whitespace. Handles both string and list inputs."""
    if not text:
        return ""
    
    # If text is a list, take the first element or join them
    if isinstance(text, list):
        if len(text) == 0:
            return ""
        text = text[0] if text else ""
    
    # Now text should be a string
    if not isinstance(text, str):
        return str(text)
    
    return " ".join(text.split())

def get_field_value(field, default=""):
    """Safely extract field value whether it's string or list."""
    if not field:
        return default
    
    if isinstance(field, list):
        return field[0] if field else default
    
    return str(field) if field else default

def display_authors(authors):
    """Format authors: if <=3 show all, else show first 3 + et al."""
    if not authors:
        return ""
    
    # Clean author names (remove extra spaces, etc.)
    cleaned_authors = []
    for a in authors:
        if isinstance(a, str):
            cleaned_authors.append(clean_text(a))
        else:
            cleaned_authors.append(str(a))
    
    if len(cleaned_authors) <= 3:
        return ", ".join(cleaned_authors)
    else:
        return ", ".join(cleaned_authors[:3]) + " et al."

def get_journal_name(pub):
    """Extract journal name from publication field"""
    if not pub:
        return ""
    
    # Handle if pub is a list
    if isinstance(pub, list):
        pub = pub[0] if pub else ""
    
    pub_str = clean_text(pub)
    
    # Common journal mappings
    journal_map = {
        "ApJ": "The Astrophysical Journal",
        "ApJL": "The Astrophysical Journal Letters",
        "ApJS": "The Astrophysical Journal Supplement Series",
        "AJ": "The Astronomical Journal",
        "MNRAS": "Monthly Notices of the Royal Astronomical Society",
        "A&A": "Astronomy & Astrophysics",
        "Nature": "Nature",
        "Science": "Science",
    }
    
    # Check if pub matches any known abbreviation
    for abbr, full_name in journal_map.items():
        if abbr in pub_str:
            return full_name
    
    return pub_str

def extract_year(pubdate):
    """Extract year from pubdate field (format: YYYY-MM-DD)"""
    if not pubdate:
        return ""
    
    # Handle if pubdate is a list
    if isinstance(pubdate, list):
        pubdate = pubdate[0] if pubdate else ""
    
    # pubdate usually comes as "2024-03-15" or just "2024"
    pubdate_str = str(pubdate)
    return pubdate_str.split("-")[0] if pubdate_str else ""

def calculate_h_index(citation_list):
    """
    Calculate h-index from a list of citation counts.
    h-index = the largest number h such that h papers have at least h citations each.
    """
    if not citation_list:
        return 0
    
    # Sort citations in descending order
    citations_sorted = sorted(citation_list, reverse=True)
    
    h_index = 0
    for i, citations in enumerate(citations_sorted, 1):
        if citations >= i:
            h_index = i
        else:
            break
    
    return h_index

def calculate_i10_index(citation_list):
    """
    Calculate i10-index = number of papers with at least 10 citations.
    """
    if not citation_list:
        return 0
    
    return sum(1 for citations in citation_list if citations >= 10)

def fetch_all_papers():
    """Fetch all papers using pagination"""
    all_papers = []
    start = 0
    rows = 50  # Number of papers per request (max is 200)
    total_found = None
    
    while True:
        # Build URL with pagination parameters
        url = (
            "https://api.adsabs.harvard.edu/v1/search/query"
            f"?q=author:%22Dihingia%22%20AND%20database:astronomy"
            f"&fl=title,author,pubdate,bibcode,citation_count,doi,pub,volume,page"
            f"&rows={rows}&start={start}"
        )
        
        # print(f"Fetching papers {start+1} to {start+rows}...")  # COMMENTED
        
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from ADS: {e}")  # Keep error messages
            return []
        
        result = r.json()
        
        if total_found is None:
            total_found = result["response"]["numFound"]
            # print(f"Total papers found: {total_found}")  # COMMENTED
        
        docs = result["response"]["docs"]
        
        if not docs:
            break
        
        all_papers.extend(docs)
        
        # Check if we've fetched all papers
        if len(all_papers) >= total_found:
            break
        
        # Move to next page
        start += rows
        
        # Safety check to prevent infinite loops
        if start > 1000:
            # print("Warning: Reached safety limit of 1000 papers")  # COMMENTED
            break
    
    # print(f"Successfully fetched {len(all_papers)} out of {total_found} papers")  # COMMENTED
    return all_papers

# print("Searching ADS for Dihingia's papers in Astronomy...")  # COMMENTED

# Fetch all papers with pagination
docs = fetch_all_papers()

if not docs:
    print("No papers found or error occurred")  # Keep error messages
    sys.exit(1)

papers = []
total_citations = 0
first_author_count = 0
many_authors_count = 0
citation_list = []  # Store all citation counts for h-index and i10-index

for p in docs:
    # Handle title (can be list or string)
    title = p.get("title", "")
    if isinstance(title, list):
        title = title[0] if title else ""
    
    # Handle authors (should be list)
    authors = p.get("author", [])
    if not isinstance(authors, list):
        authors = [authors] if authors else []
    
    citations = p.get("citation_count", 0)
    if isinstance(citations, list):
        citations = citations[0] if citations else 0
    
    # Add to citation list for h-index calculation
    citation_list.append(citations)
    
    pubdate = p.get("pubdate", "")
    pub = p.get("pub", "")
    volume = p.get("volume", "")
    page = p.get("page", "")
    
    total_citations += citations
    
    # Check if Dihingia is first author
    is_first = (
        len(authors) > 0 and 
        authors and 
        "Dihingia" in str(authors[0])
    )
    
    if is_first:
        first_author_count += 1
    
    # Check if paper has many authors (>10)
    has_many_authors = len(authors) > 10
    
    if has_many_authors:
        many_authors_count += 1
    
    # Get DOI if available
    doi = p.get("doi", "")
    if isinstance(doi, list):
        doi = doi[0] if doi else ""
    
    bibcode = p.get("bibcode", "")
    if isinstance(bibcode, list):
        bibcode = bibcode[0] if bibcode else ""
    
    url_link = f"https://doi.org/{doi}" if doi else f"https://ui.adsabs.harvard.edu/abs/{bibcode}"
    
    paper_info = {
        "title": clean_text(title),
        "url": url_link,
        "authors": [clean_text(a) for a in authors],
        "display_authors": display_authors(authors),
        "year": extract_year(pubdate),
        "journal": get_journal_name(pub),
        "volume": clean_text(volume),
        "pages": clean_text(page),
        "citations": citations,
        "bibcode": bibcode,
        "doi": doi,
        "date": get_field_value(pubdate),
        "first_author": is_first,
        "many_authors": has_many_authors,
        "num_authors": len(authors)
    }
    
    papers.append(paper_info)

# Calculate h-index and i10-index
h_index = calculate_h_index(citation_list)
i10_index = calculate_i10_index(citation_list)

# Sort papers by year (most recent first)
papers.sort(key=lambda x: x.get("year", ""), reverse=True)

# Calculate metrics with h-index and i10-index
metrics = {
    "total_publications": len(papers),
    "first_author_publications": first_author_count,
    "papers_with_many_authors": many_authors_count,
    "total_citations": total_citations,
    "h_index": h_index,
    "i10_index": i10_index,
    "average_citations_per_paper": round(total_citations / len(papers), 2) if papers else 0,
    "last_updated": datetime.now().isoformat()
}

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save publications JSON
with open("data/publications.json", "w", encoding="utf-8") as f:
    json.dump(papers, f, indent=2, ensure_ascii=False)

# Save metrics JSON with h-index and i10-index
with open("data/metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)

# All print statements below are COMMENTED out for silent operation
# print(f"\n✅ ADS update complete!")  # COMMENTED
# print(f"  - Total papers: {len(papers)}")  # COMMENTED
# print(f"  - First author papers: {first_author_count}")  # COMMENTED
# print(f"  - Papers with >10 authors: {many_authors_count}")  # COMMENTED
# print(f"  - Total citations: {total_citations}")  # COMMENTED
# print(f"  - Average citations/paper: {metrics['average_citations_per_paper']}")  # COMMENTED
# print(f"  - 📊 h-index: {h_index}")  # COMMENTED
# print(f"  - 📊 i10-index: {i10_index}")  # COMMENTED
# print(f"\n📁 Data saved to data/publications.json and data/metrics.json")  # COMMENTED

# Verify we got all papers
# if len(papers) == 60:  # COMMENTED
#     print(f"\n✅ Successfully fetched all 60 papers!")  # COMMENTED
# else:  # COMMENTED
#     print(f"\n⚠️ Warning: Expected 60 papers but fetched {len(papers)}")  # COMMENTED

# Show citation distribution (COMMENTED OUT)
# print(f"\n📊 Citation Distribution:")  # COMMENTED
# citation_ranges = [(0, 0), (1, 5), (6, 10), (11, 20), (21, 50), (51, 100), (101, float('inf'))]  # COMMENTED
# for low, high in citation_ranges:  # COMMENTED
#     if high == float('inf'):  # COMMENTED
#         count = sum(1 for c in citation_list if c >= low)  # COMMENTED
#         range_name = f"{low}+"  # COMMENTED
#     else:  # COMMENTED
#         count = sum(1 for c in citation_list if low <= c <= high)  # COMMENTED
#         range_name = f"{low}-{high}"  # COMMENTED
#     if count > 0:  # COMMENTED
#         print(f"  {range_name:8} citations: {count:2d} papers")  # COMMENTED

# Show sample of display_authors formatting (COMMENTED OUT)
# if papers:  # COMMENTED
#     print(f"\n📝 Sample of first 3 papers:")  # COMMENTED
#     for i, sample in enumerate(papers[:3], 1):  # COMMENTED
#         print(f"\n  Paper {i}:")  # COMMENTED
#         print(f"    Title: {sample['title'][:70]}..." if len(sample['title']) > 70 else f"    Title: {sample['title']}")  # COMMENTED
#         print(f"    Authors: {sample['display_authors']}")  # COMMENTED
#         print(f"    Year: {sample['year']}, Journal: {sample['journal']}")  # COMMENTED
#         print(f"    Citations: {sample['citations']}")  # COMMENTED
