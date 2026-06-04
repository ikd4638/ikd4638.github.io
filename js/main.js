fetch('data/metrics.json').then(r=>r.json()).then(d=>{
document.getElementById('pubs').innerText=d.total_publications;
document.getElementById('firstauthor').innerText=d.first_author;
document.getElementById('eht').innerText=d.eht_papers;
document.getElementById('citations').innerText=d.citations;
}).catch(()=>{});