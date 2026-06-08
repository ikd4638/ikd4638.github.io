// publications.js - Improved version with better display

let allPapers = [];
let currentFilter = 'all';
let currentSort = 'year';
let searchTerm = '';

// Load publications when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadPublications();
});

function loadPublications() {
    showLoading(true);
    
    fetch('data/publications.json')
        .then(response => response.json())
        .then(data => {
            allPapers = data;
            updateStats();
            renderPublications();
            showLoading(false);
        })
        .catch(error => {
            console.error('Error loading publications:', error);
            document.getElementById('papers').innerHTML = `
                <div class="alert alert-danger">
                    Failed to load publications. Please try again later.
                </div>
            `;
            showLoading(false);
        });
}

function updateStats() {
    const total = allPapers.length;
    const firstAuthor = allPapers.filter(p => p.first_author).length;
    const manyAuthors = allPapers.filter(p => p.many_authors).length;
    const totalCitations = allPapers.reduce((sum, p) => sum + (p.citations || 0), 0);
    
    document.getElementById('total-count').textContent = total;
    document.getElementById('first-count').textContent = firstAuthor;
    document.getElementById('many-count').textContent = manyAuthors;
    document.getElementById('total-cites').textContent = totalCitations;
}

function filterPublications(type) {
    currentFilter = type;
    
    // Update button active states
    const buttons = document.querySelectorAll('.btn-group .btn-primary');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    renderPublications();
}

function searchPublications() {
    searchTerm = document.getElementById('search-input').value.toLowerCase();
    renderPublications();
}

function sortPublications(type) {
    currentSort = type;
    
    // Update button active states
    const buttons = document.querySelectorAll('.btn-group-sm .btn-outline-secondary');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    renderPublications();
}

function getFilteredPapers() {
    let filtered = [...allPapers];
    
    // Apply filter
    if (currentFilter === 'first') {
        filtered = filtered.filter(p => p.first_author === true);
    } else if (currentFilter === 'many') {
        filtered = filtered.filter(p => p.many_authors === true);
    } else if (currentFilter === 'recent') {
        filtered = filtered.filter(p => parseInt(p.year) >= 2024);
    }
    
    // Apply search
    if (searchTerm) {
        filtered = filtered.filter(p =>
            p.title.toLowerCase().includes(searchTerm) ||
            p.journal.toLowerCase().includes(searchTerm) ||
            p.display_authors.toLowerCase().includes(searchTerm) ||
            p.year.includes(searchTerm)
        );
    }
    
    // Apply sort
    if (currentSort === 'year') {
        filtered.sort((a, b) => b.year.localeCompare(a.year));
    } else if (currentSort === 'citations') {
        filtered.sort((a, b) => (b.citations || 0) - (a.citations || 0));
    } else if (currentSort === 'title') {
        filtered.sort((a, b) => a.title.localeCompare(b.title));
    }
    
    return filtered;
}

function renderPublications() {
    const filtered = getFilteredPapers();
    const container = document.getElementById('papers');
    
    // Update result count
    document.getElementById('result-count').textContent =
        `Showing ${filtered.length} of ${allPapers.length} publications`;
    
    if (filtered.length === 0) {
        document.getElementById('no-results').style.display = 'block';
        container.innerHTML = '';
        return;
    }
    
    document.getElementById('no-results').style.display = 'none';
    
    // Render each paper as a compact card
    container.innerHTML = filtered.map(paper => `
        <div class="paper-entry">
            <div class="d-flex flex-wrap align-items-start gap-2 mb-2">
                ${paper.first_author ? '<span class="badge bg-primary">First Author</span>' : ''}
                ${paper.many_authors ? '<span class="badge bg-info">>10 Authors</span>' : ''}
                ${paper.citations && paper.citations > 50 ? '<span class="badge bg-warning text-dark">Highly Cited</span>' : ''}
                <span class="badge bg-secondary">${paper.year || 'N/A'}</span>
                ${paper.citations ? `<span class="badge bg-success">📊 ${paper.citations} citations</span>` : ''}
            </div>
            
            <h5 class="mb-2">
                <a href="${paper.url || '#'}" target="_blank" class="text-light text-decoration-none hover-primary">
                    ${paper.title || 'Untitled'}
                </a>
            </h5>
            
            <div class="authors mb-2">
                ${paper.display_authors || paper.authors?.join(', ') || 'Unknown authors'}
            </div>
            
            <div class="journal">
                ${paper.journal || 'Unknown journal'}
                ${paper.volume ? `, ${paper.volume}` : ''}
                ${paper.pages ? `, ${paper.pages}` : ''}
            </div>
        </div>
    `).join('');
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}
