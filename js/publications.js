let papers = [];

fetch("data/publications.json")
.then(response => response.json())
.then(data => {

papers = data;

render(papers);

})
.catch(error => {

console.error(
    "Could not load publications.json",
    error
);

});

function render(list){

let html = "";

list.forEach(p => {

    html += 

    <div class="card mb-3">

        <div class="card-body">

            <h5>

                <a href="${p.url || '#'}"
                   target="_blank">

                    ${p.title}

                </a>

            </h5>

            <p>

                ${p.display_authors || ""}

            </p>

            <p>

                ${p.journal || ""}

                ${p.volume ? ", Vol. " + p.volume : ""}

                ${p.pages ? ", " + p.pages : ""}

                ${p.year ? " (" + p.year + ")" : ""}

            </p>

        </div>

    </div>

    ;

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

