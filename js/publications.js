fetch('data/publications.json').then(r=>r.json()).then(ps=>{
document.getElementById('papers').innerHTML=ps.map(p=>`<p><b>${p.title}</b><br>${p.authors.join(', ')}</p>`).join('');
});