import json,os,requests
token=os.environ['ADS_API_TOKEN']
h={'Authorization':f'Bearer {token}'}
url='https://api.adsabs.harvard.edu/v1/search/query?q=author:"Dihingia"&fl=title,author,pubdate,bibcode,citation_count&rows=200'
r=requests.get(url,headers=h).json()
papers=[]
for p in r['response']['docs']:
 papers.append({'title':p.get('title',[''])[0],'authors':p.get('author',[]),'citations':p.get('citation_count',0)})
open('data/publications.json','w').write(json.dumps(papers,indent=2))
m={'total_publications':len(papers),'first_author':sum(1 for p in papers if p['authors'] and 'Dihingia' in p['authors'][0]),'eht_papers':sum(1 for p in papers if 'Event Horizon Telescope' in p['title']),'citations':sum(p['citations'] for p in papers)}
open('data/metrics.json','w').write(json.dumps(m,indent=2))
