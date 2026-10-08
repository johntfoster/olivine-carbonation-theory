/* Progressive enhancement: every review link and code snippet works without JS. */
document.querySelectorAll('[data-filter]').forEach(input => {
  const name = input.dataset.filter;
  const items = [...document.getElementById(name).querySelectorAll('.filter-item')];
  // Capture before MathJax replaces TeX with SVG: labels remain searchable.
  const text = items.map(item => item.textContent.toLowerCase());
  function filter() {
    const words = input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let shown = 0;
    items.forEach((item, i) => {
      item.hidden = !words.every(word => text[i].includes(word));
      if (!item.hidden) shown++;
    });
    document.querySelector(`[data-status="${name}"]`).textContent = `${shown} of ${items.length} shown`;
    document.querySelector(`[data-empty="${name}"]`).hidden = shown !== 0;
  }
  input.addEventListener('input', filter);
  filter();
});
const lineRange = new URLSearchParams(location.search).get('lines');
if (lineRange && /^\d+-\d+$/.test(lineRange)) {
  const [start, end] = lineRange.split('-').map(Number);
  document.querySelectorAll('.source-line').forEach(line => {
    const n = Number(line.id.slice(1));
    if (n >= start && n <= end) line.classList.add('selected-line');
  });
}
document.querySelectorAll('[data-copy-url]').forEach(button => {
  button.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(location.href); button.textContent = 'Link copied'; }
    catch (_) { button.textContent = 'Copy the address from your browser'; }
  });
});
