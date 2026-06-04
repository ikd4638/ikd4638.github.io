fetch("data/metrics.json")
.then(response => response.json())
.then(data => {

    document.getElementById("pubs").textContent =
        data.total_publications;

    document.getElementById("firstauthor").textContent =
        data.first_author;

    document.getElementById("eht").textContent =
        data.eht_papers;

    document.getElementById("citations").textContent =
        data.citations;

})
.catch(error => {
    console.log("Could not load metrics:", error);
});
