fetch("data/metrics.json")
.then(response => response.json())
.then(data => {

    document.getElementById("pubs").textContent =
    data.total_publications;

    document.getElementById("firstauthor").textContent =
    data.first_author_publications;

    document.getElementById("manyauthors").textContent =
    data.papers_with_many_authors;

    document.getElementById("citations").textContent =
    data.total_citations;

    document.getElementById("hindex").textContent =
    data.h_index;

    document.getElementById("i10index").textContent =
    data.i10_index;

    document.getElementById("lastupdated").textContent =
    new Date(data.last_updated).toLocaleDateString();
})
.catch(error => {
    console.log("Could not load metrics:", error);
});
