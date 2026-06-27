---
layout: default
permalink: /reading/
---

<section class="reading">
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
