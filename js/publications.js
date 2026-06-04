html += `
<div class="card mb-3">
  <div class="card-body">

    <h5>
      <a href="${p.url}" target="_blank">
        ${p.title}
      </a>
    </h5>

    <p>${p.display_authors}</p>

    <p>
      ${p.journal},
      ${p.volume},
      ${p.pages}
      (${p.year})
    </p>

  </div>
</div>
`;
