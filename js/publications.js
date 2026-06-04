let papers = [];

fetch("data/publications.json")
.then(r => r.json())
.then(data => {

papers = data;

render(papers);

});

function render(list){

let html = "";

list.forEach(p => {

    html += `
    <div class="card mb-3">

    <div class="card-body">

    <h5>${p.title}</h5>

    <p>
    ${p.authors.join(", ")}
    </p>

    <p>
    ${p.journal} (${p.year})
    </p>

    </div>

    </div>
    `;
});

document.getElementById("papers")
    .innerHTML = html;

}

function showAll(){
render(papers);
}

function showFirstAuthor(){

render(
    papers.filter(
        p => p.first_author
    )
);

}

function showManyAuthors(){

render(
    papers.filter(
        p => p.many_authors
    )
);

}

