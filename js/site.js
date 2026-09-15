/**
 * Loads shared layout partials when pages are not already inlined (data-static=1).
 * Server-visible pages set data-static="1" and data-inlined="true" — JS is optional.
 */
(function () {
  function basePath() {
    const base = document.body.dataset.base;
    if (base === undefined || base === "") return "";
    return base.endsWith("/") ? base : base + "/";
  }

  async function loadInto(id, url) {
    const el = document.getElementById(id);
    if (!el || !url) return;
    if (el.getAttribute("data-inlined") === "true" && el.innerHTML.trim()) return;

    try {
      const res = await fetch(basePath() + url);
      if (!res.ok) throw new Error(res.statusText);
      el.innerHTML = await res.text();
    } catch (err) {
      console.error("Layout load failed:", url, err);
      el.innerHTML =
        '<p class="p-4 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg">Could not load ' +
        url +
        '. Run the site with a local server, e.g. <code class="text-xs">python3 -m http.server</code>.</p>';
    }
  }

  function setActiveNav() {
    const page = document.body.dataset.page;
    if (!page) return;

    document.querySelectorAll("[data-nav]").forEach(function (link) {
      const isActive = link.dataset.nav === page;
      link.classList.toggle("text-ocean-600", isActive);
      link.classList.toggle("font-semibold", isActive);
      link.classList.toggle("text-gray-600", !isActive);
      if (isActive) link.setAttribute("aria-current", "page");
    });
  }

  document.addEventListener("DOMContentLoaded", async function () {
    if (document.body.dataset.static === "1") {
      setActiveNav();
      return;
    }

    const hero = document.body.dataset.hero;
    const content = document.body.dataset.content;
    const trustStrip = document.body.dataset.trustStrip;

    await Promise.all([
      loadInto("site-nav", "partials/nav.html"),
      loadInto("site-footer", "partials/footer.html"),
      loadInto("page-hero", hero),
      loadInto("page-trust-strip", trustStrip),
      loadInto("page-content", content),
    ]);

    setActiveNav();
  });
})();
