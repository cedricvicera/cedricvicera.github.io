---
layout: default
permalink: /
---

<style>
  /* ── Personal site design (inline so it ships with the page, never served
        stale by the GitHub Pages CSS cache). Overrides the base light.css. ── */
  :root {
    --paper: #f8f4ec;
    --ink: #2a2520;
    --ink-soft: #4a423a;
    --muted: #756a5d;
    --faint: #9a8c79;
    --accent: #5c5a32;        /* deep olive — section headers & link hover */
    --nav-inactive: #9a8c79;
  }
  body {
    background-color: var(--paper);
    background-image: url('{{ '/assets/images/paper-texture.png' | relative_url }}');
    background-size: 500px 500px;
    background-repeat: repeat;
    color: var(--ink);
    font-family: 'EB Garamond', Georgia, 'Times New Roman', serif;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }
  ::selection { background: #d9c7a8; }

  /* Content column (override base .layout 600px) */
  .layout {
    max-width: 660px;
    padding: clamp(26px, 6vw, 60px) clamp(22px, 6vw, 34px) clamp(48px, 8vw, 88px);
  }

  /* Header / nav (override base centered .header) */
  .header {
    display: flex;
    flex-direction: row;
    align-items: baseline;
    text-align: left;
    padding: 0 0 clamp(34px, 7vw, 60px);
  }
  .nav { display: flex; gap: 24px; align-items: baseline; flex-wrap: wrap; }
  .nav__item {
    font-family: 'EB Garamond', Georgia, 'Times New Roman', serif;
    font-size: 1.05rem;
    text-decoration: none;
    color: var(--nav-inactive);
    transition: color 0.2s ease;
  }
  .nav__item:hover,
  .nav__item.active { color: var(--ink); }

  .main { margin: 0; }

  .view { display: none; }
  .view.active { display: block; }

  .about p {
    font-size: clamp(1.18rem, 3.4vw, 1.32rem);
    line-height: 1.72;
    color: var(--ink);
    margin: 0 0 1.1em;
  }
  .about p:last-child { margin-bottom: 0; }

  .lists { display: flex; flex-direction: column; gap: clamp(38px, 6vw, 54px); }
  .lists h2 {
    font-size: clamp(1.18rem, 3.2vw, 1.32rem);
    font-weight: 600;
    letter-spacing: 0;
    color: var(--accent);
    margin: 0 0 clamp(14px, 2.4vw, 18px);
  }
  .lists ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: clamp(11px, 2vw, 14px);
  }
  .lists li { font-size: clamp(1.12rem, 3.2vw, 1.24rem); line-height: 1.4; }
  .lists li a { color: var(--ink); text-decoration: none; transition: color 0.2s ease; }
  .lists li a:hover { color: var(--accent); }
  .lists .sep { color: var(--faint); }
  .lists .author { color: var(--muted); }
</style>

<section class="view about" data-view="about">
  <p>I'm a data scientist working in AI risk and governance, building systems that monitor, assess, and quantify how risk shifts as it evolves in real time, keeping agentic deployments trustworthy at scale.</p>
</section>

<section class="view reading" data-view="reading">
  <div class="lists">
    {% for group in site.data.reading_lists %}
    <section>
      <h2>{{ group.name }}</h2>
      <ul>
        {% for book in group.books %}
        <li><a class="book-link" href="https://www.google.com/search?q={{ book.title | url_encode }}" target="_blank" rel="noopener">{{ book.title }}</a><span class="sep"> &middot; </span><span class="author">{{ book.author }}</span></li>
        {% endfor %}
      </ul>
    </section>
    {% endfor %}
  </div>
</section>

<script>
  // ----- Hash-based routing: #about (default) | #reading -----
  function show(view) {
    document.querySelectorAll('.view').forEach(function (v) {
      v.classList.toggle('active', v.dataset.view === view);
    });
    document.querySelectorAll('.nav__item').forEach(function (a) {
      a.classList.toggle('active', a.dataset.view === view);
    });
  }
  function current() {
    var h = (location.hash || '').replace('#', '');
    return h === 'reading' ? 'reading' : 'about';
  }
  window.addEventListener('hashchange', function () {
    show(current());
    window.scrollTo(0, 0);
  });
  show(current());

  // ----- Keep book links in-browser on mobile -----
  // Tapping an <a> to a Google-claimed domain triggers iOS Universal Links /
  // Android App Links, which hands the URL to the Google app. Universal Links
  // don't fire for navigation started by JavaScript, so we open the link
  // programmatically — it stays as a normal new tab in the current browser.
  document.addEventListener('click', function (e) {
    var link = e.target.closest('.book-link');
    if (!link) return;
    e.preventDefault();
    window.open(link.href, '_blank', 'noopener');
  });
</script>
