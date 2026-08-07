/* River's Edge Market — site interactions */
(function () {
  "use strict";

  /* mobile nav */
  var burger = document.querySelector(".burger");
  var mnav = document.querySelector(".mobile-nav");
  if (burger && mnav) {
    burger.addEventListener("click", function () {
      var open = mnav.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
    });
    mnav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        mnav.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      }
    });
  }

  /* highlight today's row in hours tables */
  var day = new Date().getDay(); // 0 = Sunday
  document.querySelectorAll(".hours-table tr[data-day]").forEach(function (tr) {
    if (parseInt(tr.getAttribute("data-day"), 10) === day) tr.classList.add("today");
  });

  /* scroll reveal */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.08 });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  /* shop filtering (only on pages with #product-data) */
  var dataEl = document.getElementById("product-data");
  if (!dataEl) return;

  var PRODUCTS = JSON.parse(dataEl.textContent);
  var grid = document.getElementById("shop-grid");
  var count = document.getElementById("result-count");
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chip[data-dept]"));
  var search = document.getElementById("shop-search");
  var activeDept = "all";
  var q = "";

  function money(p) {
    if (p.pm == null) return "See options";
    var a = "$" + p.pm.toFixed(2).replace(/\.00$/, "");
    if (p.px != null && p.px !== p.pm) a += " – $" + p.px.toFixed(2).replace(/\.00$/, "");
    return a;
  }

  function render() {
    var ql = q.trim().toLowerCase();
    var shown = PRODUCTS.filter(function (p) {
      var okDept = activeDept === "all" || p.d.indexOf(activeDept) > -1;
      var okQ = !ql || p.n.toLowerCase().indexOf(ql) > -1 || p.c.toLowerCase().indexOf(ql) > -1;
      return okDept && okQ;
    });
    var html = shown.map(function (p) {
      var img = p.i
        ? '<img src="' + p.i + '?width=600" srcset="' + p.i + '?width=400 400w, ' + p.i + '?width=600 600w, ' + p.i + '?width=900 900w" sizes="(max-width:620px) 46vw, (max-width:1020px) 30vw, 280px" alt="' + p.n.replace(/"/g, "&quot;") + '" loading="lazy" decoding="async">'
        : '<img src="' + (window.PLACEHOLDER || "assets/placeholder.svg") + '" alt="' + p.n.replace(/"/g, "&quot;") + '" loading="lazy">';
      return '<a class="card" href="' + p.u + '" target="_blank" rel="noopener">' +
        '<div class="card-img">' + img + "</div>" +
        '<div class="card-body"><span class="card-cat">' + p.c + "</span>" +
        '<span class="card-name">' + p.n + "</span>" +
        '<span class="card-price"><span>' + money(p) + '</span><span class="shop-tag">Shop</span></span>' +
        "</div></a>";
    }).join("");
    grid.innerHTML = html || '<p style="grid-column:1/-1;color:var(--ink-soft);padding:2rem 0;">No pieces match — try a different search.</p>';
    if (count) count.textContent = shown.length + " of " + PRODUCTS.length + " pieces";
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (c) { c.classList.remove("active"); });
      chip.classList.add("active");
      activeDept = chip.getAttribute("data-dept");
      render();
    });
  });
  if (search) search.addEventListener("input", function () { q = search.value; render(); });

  /* deep-link: shop.html?dept=Apparel or #apparel */
  var params = new URLSearchParams(location.search);
  var want = params.get("dept");
  if (want) {
    var match = chips.filter(function (c) { return c.getAttribute("data-dept") === want; })[0];
    if (match) match.click();
  }
  render();
})();
