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
.books-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
@media (min-width: 600px) {
  .books-grid { grid-template-columns: repeat(7, 1fr); }
}

.book-item {
  position: relative; cursor: pointer; border-radius: 6px;
  overflow: hidden; aspect-ratio: 2/3; background: #d6d3cf;
  box-shadow: 0 0 0 1px rgba(0,0,0,0.1);
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
  box-shadow: 0 0 0 1px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.18);
  z-index: 10;
}
.book-item img { width: 100%; height: 100%; object-fit: cover; display: block; }
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
.book-tooltip b { display: block; font-weight: 600; font-size: 0.58rem; color: #ffffff; }
.book-tooltip span { font-style: italic; color: #aaaaaa; font-size: 0.53rem; }
.book-placeholder {
  width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
  padding: 6px; text-align: center; font-size: 0.45rem; color: #5c5c5c; line-height: 1.3;
}

/* Spine mode */
.bookshelf.spine-mode .books-grid { grid-template-columns: 1fr; gap: 0; }
.bookshelf.spine-mode .book-item {
  aspect-ratio: unset; height: auto; border-radius: 0; overflow: visible;
  background: none !important; box-shadow: none !important; animation: none;
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

<div class="bookshelf" id="shelf">
  <div class="books-grid">
    {% for book in site.data.books %}
    <div class="book-item" style="animation-delay: {{ forloop.index0 | times: 30 }}ms">
      <img
        src="{{ '/assets/images/books/' | append: book.isbn | append: '.jpg' | relative_url }}"
        data-fallback="https://covers.openlibrary.org/b/isbn/{{ book.isbn }}-L.jpg"
        alt="{{ book.title }}"
        loading="lazy"
        onerror="if(this.src!==this.dataset.fallback){this.src=this.dataset.fallback;}else{this.style.display='none';var p=this.parentNode;if(!p.querySelector('.book-placeholder')){var d=document.createElement('div');d.className='book-placeholder';d.textContent=this.alt;p.prepend(d);}}"
      >
      <div class="book-tooltip">
        <b>{{ book.title }}</b><span>{{ book.author }}</span>
      </div>
      <div class="spine-label">
        <span class="spine-label__title">{{ book.title }}</span>
        <span class="spine-label__author">{{ book.author }}</span>
      </div>
    </div>
    {% endfor %}
  </div>
</div>

<script>
let spineMode = false;
const shelf = document.getElementById('shelf');
const coverBtn = document.getElementById('coverBtn');
const spineBtn = document.getElementById('spineBtn');

document.querySelectorAll('.book-item').forEach(function(item) {
  item.addEventListener('click', function() {
    if (!spineMode) return;
    var title = item.querySelector('.spine-label__title').textContent;
    var author = item.querySelector('.spine-label__author').textContent;
    navigator.clipboard.writeText(title + ' \u2014 ' + author).then(function() {
      var label = item.querySelector('.spine-label');
      label.style.opacity = '0.4';
      setTimeout(function() { label.style.opacity = ''; }, 400);
    });
  });
});

coverBtn.addEventListener('click', function() {
  if (spineMode) {
    spineMode = false;
    shelf.classList.remove('spine-mode');
    coverBtn.classList.add('active');
    spineBtn.classList.remove('active');
  }
});
spineBtn.addEventListener('click', function() {
  if (!spineMode) {
    spineMode = true;
    shelf.classList.add('spine-mode');
    spineBtn.classList.add('active');
    coverBtn.classList.remove('active');
  }
});
</script>
