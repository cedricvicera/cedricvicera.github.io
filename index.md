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
      <p>Immersing in literary, filmic, and technological landscapes.</p>
    </div>
  </div>
</div>

<script src="{{ '/assets/js/wave-animation.js' | relative_url }}"></script>

<style>
.bio { font-size: 16px; }

/* ── Header row ── */
.books-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 16px; margin-top: 48px;
}
.books-label {
  font-family: 'Inter', -apple-system, sans-serif; font-size: 0.7rem;
  font-weight: 400; letter-spacing: 0.12em; text-transform: uppercase; color: #5c5c5c;
}

/* ── Breakout: escape the 600px layout to ~1050px ── */
.books-breakout {
  box-sizing: border-box;
}
.books-breakout.cover-mode {
  width: min(1050px, 100vw);
  margin-left: calc((min(600px, 100vw) - min(1050px, 100vw)) / 2 - 15px);
  padding: 0 15px;
}
.books-breakout:not(.cover-mode) {
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 15px;
}
@media (max-width: 700px) {
  .books-breakout.cover-mode {
    width: auto;
    margin-left: 0;
    margin-right: 0;
    padding: 0;
  }
}

/* ── Cover grid ── */
.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(135px, 1fr));
  gap: 12px;
}

/* ── Book tile ── */
.book-item {
  position: relative; cursor: pointer;
  overflow: visible; /* keep visible so tooltip escapes */
  transform-origin: bottom center;
  transition: transform 0.2s cubic-bezier(.22,.68,0,1.2);
  animation: bookIn 0.4s both ease-out;
}
@keyframes bookIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.book-item:hover { transform: translateY(-6px) scale(1.04); z-index: 10; }

/* ── Cover image wrapper ── */
.book-cover-wrap {
  position: relative;
  width: 100%;
  padding-top: 150%;
}
.book-cover-wrap img {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  object-fit: cover; display: block;
  border-radius: 8px;
  box-shadow: 0 0 0 1.5px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.08);
  transition: box-shadow 0.2s ease;
}
.book-item:hover .book-cover-wrap img {
  box-shadow: 0 0 0 1.5px rgba(0,0,0,0.12), 0 8px 20px rgba(0,0,0,0.15);
}
.book-cover-wrap .book-placeholder {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  padding: 6px; text-align: center; font-size: 0.45rem; color: #5c5c5c; line-height: 1.3;
  border-radius: 8px; background: #e8e5e1;
  box-shadow: 0 0 0 1.5px rgba(0,0,0,0.12);
}

/* ── Hover tooltip ── */
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
.book-tooltip b { display: block; font-weight: 600; font-size: 0.58rem; color: #fff; }
.book-tooltip span { font-style: italic; color: #aaa; font-size: 0.53rem; }

.book-item a {
  display: block; text-decoration: none; color: inherit;
}
</style>

<div class="books-breakout cover-mode" id="books-breakout">
<div class="books-header">
  <span class="books-label">Book recommendations</span>
</div>
<div class="bookshelf" id="shelf">
  <div class="books-grid">
    {% for book in site.data.books %}
    <div class="book-item" style="animation-delay: {{ forloop.index0 | times: 30 }}ms">
      <a href="https://www.google.com/search?q={{ book.title | url_encode }}" target="_blank" rel="noopener">
        <div class="book-cover-wrap">
          {% if book.cover %}
            {% assign cover_file = book.cover %}
          {% else %}
            {% assign cover_file = book.isbn | append: '.jpg' %}
          {% endif %}
          <img
            src="{{ '/assets/images/books/' | append: cover_file | relative_url }}"
            alt="{{ book.title }}"
            loading="lazy"
            onerror="this.style.display='none';var p=this.parentNode;if(!p.querySelector('.book-placeholder')){var d=document.createElement('div');d.className='book-placeholder';d.textContent='{{ book.title }}';p.appendChild(d);}"
          >
        </div>
        <div class="book-tooltip">
          <b>{{ book.title }}</b><span>{{ book.author }}</span>
        </div>
      </a>
    </div>
    {% endfor %}
  </div>
</div>
</div>
