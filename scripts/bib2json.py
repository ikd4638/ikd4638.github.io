import json
import re

bibfile = "data/All-publications.bib"

with open(bibfile, "r", encoding="utf-8") as f:
     text = f.read()

entries = re.split(r'@\w+\{', text)[1:]

papers = []

for entry in entries:

    title = ""
    authors = ""
    year = ""
    journal = ""

m = re.search(r'title\\s*=\\s*\\{(.*?)\\}', entry, re.S)
if m:
    title = m.group(1).replace("\\n", " ")

m = re.search(r'author\\s*=\\s*\\{(.*?)\\}', entry, re.S)
if m:
    authors = m.group(1)

m = re.search(r'year\\s*=\\s*\\{(.*?)\\}', entry)
if m:
    year = m.group(1)

m = re.search(r'journal\\s*=\\s*\\{(.*?)\\}', entry)
if m:
    journal = m.group(1)

author_list = [a.strip() for a in authors.split(" and ")]

papers.append({
    "title": title,
    "authors": author_list,
    "year": year,
    "journal": journal,
    "first_author":
        len(author_list) > 0
        and "Dihingia" in author_list[0],

    "many_authors":
        len(author_list) > 10
})

papers.sort(
key=lambda x: x["year"],
reverse=True
)

with open("data/publications.json", "w") as f:
     json.dump(papers, f, indent=2)

