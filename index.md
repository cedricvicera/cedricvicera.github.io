---
layout: page
permalink: /
---

<div class="home-container">
  <!-- Wave Animation Canvas - Rectangular Format -->
  <div class="wave-animation-wrapper">
    <canvas id="wave-canvas" width="800" height="300"></canvas>
  </div>
  
  <!-- Content (no name since header has it) -->
  <div class="content">
    <div class="bio">
      <p>I work in data science and analytics.</p>
      <p>Previously, I studied philosophy and computer science.</p>
    </div>
  </div>
</div>

<script src="{{ '/assets/js/wave-animation.js' | relative_url }}"></script>

<style>
.books-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  margin-top: 48px;
}
.books-label {
  font-family: 'Inter', -apple-system, sans-serif;
  font-size: 0.7rem;
  font-weight: 400;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #5c5c5c;
}
.view-toggle { display: flex; gap: 6px; align-items: center; }
.view-btn {
  border: none; background: none; padding: 4px; cursor: pointer;
  color: #d6d6d6; border-radius: 3px; display: flex; align-items: center;
  transition: color 0.15s;
}
.view-btn.active { color: #1b813e; }
.view-btn:hover { color: #1c1c1c; }
.view-btn svg { display: block; }

.bookshelf { position: relative; }
.books-header, .bookshelf {
  width: 100%;
  box-sizing: border-box;
}
.shelf-row { position: relative; }
.shelf-row::after {
  content: '';
  display: block;
  height: 3px;
  background: linear-gradient(180deg, #d4cfc9 0%, transparent 100%);
  border-radius: 0 0 2px 2px;
  margin-top: 2px;
}
.no-shelves .shelf-row::after { display: none !important; }
.books-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 5px; }
@media (min-width: 600px) {
  .books-grid { grid-template-columns: repeat(7, 1fr); }
}

.book-item {
  position: relative; cursor: pointer; border-radius: 2px;
  overflow: visible; aspect-ratio: 2/3; background: #e0dbd5;
  transform-origin: bottom center;
  transition: transform 0.2s cubic-bezier(.22,.68,0,1.2), box-shadow 0.2s ease;
  animation: bookIn 0.4s both ease-out;
}
@keyframes bookIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.book-item:hover {
  transform: translateY(-6px) scale(1.04);
  box-shadow: 0 12px 24px rgba(0,0,0,0.18);
  z-index: 10;
}
.book-item img { width: 100%; height: 100%; object-fit: cover; display: block; border-radius: 2px; }
.book-tooltip {
  position: absolute; bottom: calc(100% + 8px); left: 50%; transform: translateX(-50%);
  background: #1c1c1c; color: white; padding: 5px 8px; border-radius: 4px;
  font-size: 0.55rem; font-family: 'Inter', sans-serif;
  pointer-events: none; opacity: 0; transition: opacity 0.15s;
  z-index: 20; text-align: center; max-width: 120px; white-space: normal; line-height: 1.4;
}
.book-tooltip::after {
  content: ''; position: absolute; top: 100%; left: 50%; transform: translateX(-50%);
  border: 4px solid transparent; border-top-color: #1c1c1c;
}
.book-item:hover .book-tooltip { opacity: 1; }
.book-tooltip b { display: block; font-weight: 600; font-size: 0.58rem; }
.book-tooltip span { font-style: italic; opacity: 0.75; font-size: 0.53rem; }
.book-placeholder {
  width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
  padding: 6px; text-align: center; font-size: 0.45rem; color: #5c5c5c; line-height: 1.3;
}

/* Spine mode */
.bookshelf.spine-mode .shelf-row::after { display: none; }
.bookshelf.spine-mode .books-grid { grid-template-columns: 1fr; gap: 0; }
.bookshelf.spine-mode .book-item {
  aspect-ratio: unset; height: auto; border-radius: 0; overflow: visible;
  background: none !important; animation: none;
  border-bottom: 1px solid #d6d6d6; transition: background 0.15s;
}
.bookshelf.spine-mode .book-item:first-child { border-top: 1px solid #d6d6d6; }
.bookshelf.spine-mode .book-item:hover {
  transform: none; box-shadow: none; background: rgba(0,0,0,0.025) !important;
}
.bookshelf.spine-mode .book-item img { display: none; }
.bookshelf.spine-mode .book-tooltip { display: none; }
.spine-label {
  display: none; align-items: baseline; padding: 10px 0;
  pointer-events: none; position: static; inset: unset;
}
.bookshelf.spine-mode .spine-label { display: flex; }
.spine-label__title {
  font-size: 0.8rem; font-family: 'Inter', -apple-system, sans-serif;
  font-weight: 400; color: #1c1c1c; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.spine-label__author {
  font-size: 0.75rem; font-family: 'Palatino', 'Book Antiqua', serif;
  font-style: italic; color: #5c5c5c; white-space: nowrap; overflow: hidden;
  text-overflow: ellipsis; margin-left: auto; padding-left: 16px; flex-shrink: 0;
}
</style>

<div class="books-header">
  <span class="books-label">Book recommendations</span>
  <div class="view-toggle">
    <button class="view-btn active" id="coverBtn" title="Cover view" aria-label="Cover view">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <rect x="1" y="1" width="6" height="6" rx="1" fill="currentColor"/>
        <rect x="9" y="1" width="6" height="6" rx="1" fill="currentColor"/>
        <rect x="1" y="9" width="6" height="6" rx="1" fill="currentColor"/>
        <rect x="9" y="9" width="6" height="6" rx="1" fill="currentColor"/>
      </svg>
    </button>
    <button class="view-btn" id="spineBtn" title="Spine view" aria-label="Spine view">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <rect x="1" y="2" width="14" height="2.5" rx="1" fill="currentColor"/>
        <rect x="1" y="6.75" width="14" height="2.5" rx="1" fill="currentColor"/>
        <rect x="1" y="11.5" width="14" height="2.5" rx="1" fill="currentColor"/>
      </svg>
    </button>
  </div>
</div>

<div class="bookshelf" id="shelf"></div>

<script>
const books = [
  { title: "Liberty, Equality, Fraternity",    author: "James Fitzjames Stephen",   isbn: "0865971358" },
  { title: "Beethoven",                         author: "Maynard Solomon",            isbn: "0028706439" },
  { title: "1939: The Last World of the Fair",  author: "David Gelernter",            isbn: "0684831392" },
  { title: "The House of Intellect",            author: "Jacques Barzun",             isbn: "0060970308" },
  { title: "Don Quixote",                       author: "Miguel de Cervantes",        isbn: "0060934344" },
  { title: "The True Believer",                 author: "Eric Hoffer",                isbn: "0060505915" },
  { title: "The Long Loneliness",               author: "Dorothy Day",                isbn: "0060617519" },
  { title: "Confessions of a 20th-C Pilgrim",  author: "Malcolm Muggeridge",         isbn: "0060657685" },
  { title: "The Gulag Archipelago",             author: "Aleksandr Solzhenitsyn",     isbn: "0061253723" },
  { title: "Anathem",                           author: "Neal Stephenson",            isbn: "0061492302" },
  { title: "The First Circle",                  author: "Aleksandr Solzhenitsyn",     isbn: "0061340766" },
  { title: "Paul: A Biography",                 author: "N.T. Wright",                isbn: "0062279246" },
  { title: "Road to Disaster",                  author: "Brian VanDeMark",            isbn: "0316415383" },
  { title: "Till We Have Faces",                author: "C.S. Lewis",                 isbn: "0156904365" },
  { title: "C.S. Lewis Signature Classics",     author: "C.S. Lewis",                isbn: "0060653191" },
  { title: "With God in Russia",                author: "Walter J. Ciszek",           isbn: "0898700620" },
  { title: "The Perfectionists",                author: "Simon Winchester",           isbn: "0062655639" },
  { title: "The Good Soldier \u0160vejk",       author: "Jaroslav Ha\u0161ek",        isbn: "0140449248" },
  { title: "From Puritanism to Postmodernism",  author: "Ruland & Bradbury",          isbn: "0140174265" },
  { title: "Cadillac Desert",                   author: "Marc Reisner",               isbn: "0140178936" },
  { title: "The Odyssey",                       author: "Homer (tr. Robert Fagles)",  isbn: "0140268863" },
];

const COLS = 7, GAP = 5;
let spineMode = false;

const shelf = document.getElementById('shelf');
const coverBtn = document.getElementById('coverBtn');
const spineBtn = document.getElementById('spineBtn');

function makeBookItem(book, delay) {
  const item = document.createElement('div');
  item.className = 'book-item';
  item.style.animationDelay = delay + 'ms';

  const img = document.createElement('img');
  img.alt = book.title;
  img.loading = 'lazy';
  img.src = 'https://covers.openlibrary.org/b/isbn/' + book.isbn + '-M.jpg';
  img.onerror = function() {
    this.style.display = 'none';
    if (!item.querySelector('.book-placeholder')) {
      const ph = document.createElement('div');
      ph.className = 'book-placeholder';
      ph.textContent = book.title;
      item.prepend(ph);
    }
  };

  const tooltip = document.createElement('div');
  tooltip.className = 'book-tooltip';
  tooltip.innerHTML = '<b>' + book.title + '</b><span>' + book.author + '</span>';

  const spineLabel = document.createElement('div');
  spineLabel.className = 'spine-label';
  spineLabel.innerHTML =
    '<span class="spine-label__title">' + book.title + '</span>' +
    '<span class="spine-label__author">' + book.author + '</span>';

  item.addEventListener('click', function() {
    if (!spineMode) return;
    var text = book.title + ' — ' + book.author;
    navigator.clipboard.writeText(text).then(function() {
      spineLabel.style.opacity = '0.4';
      setTimeout(function() { spineLabel.style.opacity = ''; }, 400);
    });
  });

  item.appendChild(img);
  item.appendChild(tooltip);
  item.appendChild(spineLabel);
  return item;
}

function buildCoverShelf() {
  shelf.innerHTML = '';
  shelf.classList.remove('spine-mode', 'no-shelves');
  var row = document.createElement('div');
  row.className = 'shelf-row';
  var grid = document.createElement('div');
  grid.className = 'books-grid';
  books.forEach(function(book, i) {
    grid.appendChild(makeBookItem(book, i * 30));
  });
  row.appendChild(grid);
  shelf.appendChild(row);
}

function buildSpineShelf() {
  shelf.innerHTML = '';
  shelf.classList.add('spine-mode');
  var row = document.createElement('div');
  row.className = 'shelf-row';
  var grid = document.createElement('div');
  grid.className = 'books-grid';
  books.forEach(function(book, i) { grid.appendChild(makeBookItem(book, 0)); });
  row.appendChild(grid);
  shelf.appendChild(row);
}

buildCoverShelf();

coverBtn.addEventListener('click', function() {
  if (spineMode) { spineMode = false; coverBtn.classList.add('active'); spineBtn.classList.remove('active'); buildCoverShelf(); }
});
spineBtn.addEventListener('click', function() {
  if (!spineMode) { spineMode = true; spineBtn.classList.add('active'); coverBtn.classList.remove('active'); buildSpineShelf(); }
});
</script>
