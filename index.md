---
layout: default
permalink: /
---

<section class="view about" data-view="about">
  <p>I'm a data scientist working in AI risk and governance &mdash; building systems that monitor, assess, and quantify how risk shifts as AI evolves in real time, keeping agentic systems trustworthy at scale.</p>
</section>

<section class="view reading" data-view="reading">
  <div class="lists">
    {% for group in site.data.reading_lists %}
    <section>
      <h2>{{ group.name }}</h2>
      <ul>
        {% for book in group.books %}
        <li><a href="https://www.google.com/search?q={{ book.title | url_encode }}" target="_blank" rel="noopener">{{ book.title }}</a><span class="sep"> &middot; </span><span class="author">{{ book.author }}</span></li>
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
</script>
