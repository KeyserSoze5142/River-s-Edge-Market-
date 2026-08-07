#!/usr/bin/env python3
"""Static site generator for the new River's Edge Market website."""
import json, os, shutil, html, datetime
from config import (SITE_BASE, PRODUCT_BASE, GIFT_CARD_URL, BUSINESS, HOURS,
                    SOCIALS, COLLECTIONS, DEPARTMENTS, BRANDS)

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
OUT = os.path.join(ROOT, "site")

with open(os.path.join(ROOT, "data", "products.json")) as f:
    PRODUCTS = json.load(f)

BY_ID = {p["id"]: p for p in PRODUCTS}

def esc(s):
    return html.escape(str(s), quote=True)

def money(p):
    if p["priceMin"] is None:
        return "See options"
    a = "${:,.2f}".format(p["priceMin"]).replace(".00", "")
    if p["priceMax"] and p["priceMax"] != p["priceMin"]:
        a += " – " + "${:,.2f}".format(p["priceMax"]).replace(".00", "")
    return a

def dept_of(p):
    for c in p["cats"]:
        if c in COLLECTIONS:
            return COLLECTIONS[c][1]
    return "Gifts"

def primary_collection(p):
    for c in p["cats"]:
        if c in COLLECTIONS:
            return COLLECTIONS[c][0]
    return "Boutique"

def img_tag(p, sizes="(max-width:620px) 46vw, (max-width:1020px) 30vw, 280px", eager=False):
    load = "" if eager else ' loading="lazy" decoding="async"'
    if p["image"]:
        i = p["image"]
        return ('<img src="%s?width=600" srcset="%s?width=400 400w, %s?width=600 600w, %s?width=900 900w" '
                'sizes="%s" alt="%s"%s>') % (i, i, i, i, sizes, esc(p["name"]), load)
    return '<img src="%sassets/placeholder.svg" alt="%s"%s>' % ("../" if CTX["depth"] else "", esc(p["name"]), load)

CTX = {"depth": 0}  # 0 = root pages, 1 = collections/

def rel(path):
    return ("../" if CTX["depth"] else "") + path

def card(p):
    url = PRODUCT_BASE + p["url"]
    return ('<a class="card" href="%s" target="_blank" rel="noopener">'
            '<div class="card-img">%s</div>'
            '<div class="card-body"><span class="card-cat">%s</span>'
            '<span class="card-name">%s</span>'
            '<span class="card-price"><span>%s</span><span class="shop-tag">Shop</span></span>'
            '</div></a>') % (url, img_tag(p), esc(primary_collection(p)), esc(p["name"]), money(p))

# ---------------------------------------------------------------- SVG icons
ICONS = {
    "Facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.1c0-.9.3-1.5 1.6-1.5h1.3V4.9c-.6-.1-1.4-.2-2.3-.2-2.3 0-3.9 1.4-3.9 4v2.3H7.9v3h2.3v7h3.3z"/></svg>',
    "Instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4.3c2.5 0 2.8 0 3.8.1 1 0 1.5.2 1.8.3.5.2.8.4 1.1.7.3.3.6.7.7 1.1.1.3.3.9.3 1.8.1 1 .1 1.3.1 3.8s0 2.8-.1 3.8c0 1-.2 1.5-.3 1.8-.2.5-.4.8-.7 1.1-.3.3-.7.6-1.1.7-.3.1-.9.3-1.8.3-1 .1-1.3.1-3.8.1s-2.8 0-3.8-.1c-1 0-1.5-.2-1.8-.3-.5-.2-.8-.4-1.1-.7-.3-.3-.6-.7-.7-1.1-.1-.3-.3-.9-.3-1.8-.1-1-.1-1.3-.1-3.8s0-2.8.1-3.8c0-1 .2-1.5.3-1.8.2-.5.4-.8.7-1.1.3-.3.7-.6 1.1-.7.3-.1.9-.3 1.8-.3 1-.1 1.3-.1 3.8-.1zM12 2.5c-2.6 0-2.9 0-3.9.1-1 0-1.7.2-2.3.4-.6.3-1.2.6-1.7 1.1-.5.5-.9 1.1-1.1 1.7-.2.6-.4 1.3-.4 2.3-.1 1-.1 1.3-.1 3.9s0 2.9.1 3.9c0 1 .2 1.7.4 2.3.3.6.6 1.2 1.1 1.7.5.5 1.1.9 1.7 1.1.6.2 1.3.4 2.3.4 1 .1 1.3.1 3.9.1s2.9 0 3.9-.1c1 0 1.7-.2 2.3-.4.6-.3 1.2-.6 1.7-1.1.5-.5.9-1.1 1.1-1.7.2-.6.4-1.3.4-2.3.1-1 .1-1.3.1-3.9s0-2.9-.1-3.9c0-1-.2-1.7-.4-2.3-.3-.6-.6-1.2-1.1-1.7-.5-.5-1.1-.9-1.7-1.1-.6-.2-1.3-.4-2.3-.4-1-.1-1.3-.1-3.9-.1zm0 4.6a4.9 4.9 0 100 9.8 4.9 4.9 0 000-9.8zm0 8.1a3.2 3.2 0 110-6.4 3.2 3.2 0 010 6.4zm6.2-8.3a1.1 1.1 0 11-2.3 0 1.1 1.1 0 012.3 0z"/></svg>',
    "TikTok": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 3c.3 1.7 1.4 3 3.4 3.2v2.6c-1.3 0-2.5-.4-3.4-1v6.4c0 3.3-2.3 5.8-5.6 5.8A5.5 5.5 0 015.5 14c0-3.1 2.4-5.6 5.6-5.6l.9.1v2.7l-.9-.1a2.8 2.8 0 100 5.6c1.7 0 2.9-1.2 2.9-3.2V3h2.6z"/></svg>',
}

def socials_html():
    out = []
    for name, url in SOCIALS.items():
        out.append('<a href="%s" target="_blank" rel="noopener" aria-label="%s">%s</a>' % (url, name, ICONS[name]))
    return '<div class="socials">%s</div>' % "".join(out)

# ---------------------------------------------------------------- chrome
def collections_by_dept():
    g = {}
    for slug, (name, dept, blurb) in COLLECTIONS.items():
        g.setdefault(dept, []).append((slug, name))
    return g

def nav_drop():
    g = collections_by_dept()
    cols = []
    for dept in DEPARTMENTS:
        if dept not in g:
            continue
        links = "".join('<a href="%scollections/%s.html">%s</a>' % (rel(""), s, esc(n)) for s, n in g[dept])
        cols.append('<div class="drop-group"><div class="drop-title">%s</div>%s</div>' % (esc(dept), links))
    return "".join(cols)

def header(active=""):
    def cur(k):
        return ' aria-current="page"' if active == k else ""
    r = rel("")
    g = collections_by_dept()
    m_groups = []
    for dept in DEPARTMENTS:
        if dept not in g:
            continue
        links = "".join('<a href="%scollections/%s.html">%s</a>' % (r, s, esc(n)) for s, n in g[dept])
        m_groups.append('<div class="m-group">%s</div><div class="m-sub">%s</div>' % (esc(dept), links))
    return """
<div class="announce">Complimentary shipping on orders over <strong>$150</strong> &nbsp;·&nbsp; Local pickup in Tuscaloosa</div>
<header class="site-header">
  <div class="wrap nav-inner">
    <a class="brand" href="%(r)sindex.html" aria-label="River's Edge Market home">
      <span class="brand-name">River&rsquo;s Edge Market</span>
      <span class="brand-sub">Tuscaloosa &middot; Est. %(founded)s</span>
    </a>
    <nav aria-label="Primary">
      <ul class="nav-links">
        <li><a class="nav-link" href="%(r)sindex.html"%(c_home)s>Home</a></li>
        <li><a class="nav-link" href="%(r)sshop.html"%(c_shop)s>Shop All</a></li>
        <li class="has-drop">
          <button aria-haspopup="true">Collections</button>
          <div class="drop">%(drop)s</div>
        </li>
        <li><a class="nav-link" href="%(r)sabout.html"%(c_about)s>Our Story</a></li>
        <li><a class="nav-link" href="%(r)scontact.html"%(c_contact)s>Visit Us</a></li>
      </ul>
    </nav>
    <a class="nav-cta" href="%(gift)s" target="_blank" rel="noopener">Gift Cards</a>
    <button class="burger" aria-expanded="false" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</header>
<nav class="mobile-nav" aria-label="Mobile">
  <a href="%(r)sindex.html">Home</a>
  <a href="%(r)sshop.html">Shop All</a>
  <a href="%(r)sabout.html">Our Story</a>
  <a href="%(r)scontact.html">Visit Us</a>
  <a href="%(gift)s" target="_blank" rel="noopener">Gift Cards</a>
  %(mgroups)s
</nav>
""" % {"r": r, "drop": nav_drop(), "gift": GIFT_CARD_URL, "founded": BUSINESS["founded"],
       "c_home": cur("home"), "c_shop": cur("shop"), "c_about": cur("about"), "c_contact": cur("contact"),
       "mgroups": "".join(m_groups)}

def hours_rows():
    rows = []
    daymap = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}
    for day, span in HOURS:
        if span:
            t = "%s – %s" % (fmt12(span[0]), fmt12(span[1]))
        else:
            t = '<span class="closed">Closed</span>'
        rows.append('<tr data-day="%d"><td>%s</td><td>%s</td></tr>' % (daymap[day], day, t))
    return "".join(rows)

def fmt12(t):
    h, m = t.split(":")
    h = int(h)
    suf = "AM" if h < 12 else "PM"
    h12 = h if 1 <= h <= 12 else abs(h - 12)
    return "%d:%s %s" % (h12, m, suf)

def footer():
    r = rel("")
    g = collections_by_dept()
    col_links = []
    for dept in DEPARTMENTS[:4]:
        for s, n in g.get(dept, [])[:2]:
            col_links.append('<li><a href="%scollections/%s.html">%s</a></li>' % (r, s, esc(n)))
    year = datetime.date.today().year
    return """
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="f-brand">River&rsquo;s Edge Market</div>
        <p class="f-tag">An upscale boutique for home d&eacute;cor, women&rsquo;s fashion, and gifts — rooted in West Alabama since %(founded)s.</p>
        %(socials)s
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="%(r)sshop.html">Shop All</a></li>
          <li><a href="%(r)sabout.html">Our Story</a></li>
          <li><a href="%(r)sfaq.html">FAQ</a></li>
          <li><a href="%(r)scontact.html">Visit Us</a></li>
          <li><a href="%(gift)s" target="_blank" rel="noopener">Gift Cards</a></li>
        </ul>
      </div>
      <div>
        <h4>Collections</h4>
        <ul>%(cols)s</ul>
      </div>
      <div>
        <h4>Visit</h4>
        <ul>
          <li>%(street)s</li>
          <li>%(city)s, %(region)s %(zip)s</li>
          <li><a href="tel:%(phone_e164)s">%(phone)s</a></li>
          <li><a href="mailto:%(email)s">%(email)s</a></li>
          <li>Tue&ndash;Fri 10&ndash;5 &middot; Sat 10&ndash;2</li>
        </ul>
      </div>
    </div>
    <div class="footer-base">
      <span>&copy; %(year)s %(legal)s &middot; %(city)s, Alabama</span>
      <span>Secure checkout by Square &middot; Visa &middot; Mastercard &middot; Amex &middot; Apple&nbsp;Pay &middot; Google&nbsp;Pay</span>
    </div>
  </div>
</footer>
<script src="%(r)sassets/app.js" defer></script>
""" % {"r": r, "socials": socials_html(), "gift": GIFT_CARD_URL, "year": year,
       "cols": "".join(col_links), "founded": BUSINESS["founded"], "legal": BUSINESS["legal"],
       "street": BUSINESS["street"], "city": BUSINESS["city"], "region": BUSINESS["region"],
       "zip": BUSINESS["zip"], "phone": BUSINESS["phone"], "phone_e164": BUSINESS["phone_e164"],
       "email": BUSINESS["email"]}

def head(title, desc, path, jsonld=None, ogimg=None):
    r = rel("")
    canonical = SITE_BASE + "/" + path
    og = ogimg or (SITE_BASE + "/assets/og-cover.jpg")
    ld = ""
    if jsonld:
        for block in jsonld:
            ld += '<script type="application/ld+json">%s</script>\n' % json.dumps(block, ensure_ascii=False)
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canonical)s">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#103A39">
<meta property="og:type" content="website">
<meta property="og:site_name" content="River's Edge Market">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(og)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(og)s">
<link rel="icon" type="image/svg+xml" href="%(r)sassets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://131443099.cdn6.editmysite.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Jost:ital,wght@0,300..600;1,300..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%(r)sassets/styles.css">
%(ld)s</head>
<body>
""" % {"title": esc(title), "desc": esc(desc), "canonical": canonical, "og": og, "r": r, "ld": ld}

# ---------------------------------------------------------------- JSON-LD
def ld_store():
    hours_spec = []
    for day, span in HOURS:
        if span:
            hours_spec.append({
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": day, "opens": span[0], "closes": span[1],
            })
    return {
        "@context": "https://schema.org",
        "@type": "Store",
        "@id": SITE_BASE + "/#store",
        "name": BUSINESS["name"],
        "description": "Upscale boutique in Tuscaloosa, Alabama offering home decor, home fragrance, women's fashion, jewelry, leather goods, and gifts.",
        "url": SITE_BASE + "/",
        "telephone": BUSINESS["phone_e164"],
        "email": BUSINESS["email"],
        "priceRange": "$$",
        "image": SITE_BASE + "/assets/og-cover.jpg",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": BUSINESS["street"],
            "addressLocality": BUSINESS["city"],
            "addressRegion": BUSINESS["region"],
            "postalCode": BUSINESS["zip"],
            "addressCountry": "US",
        },
        "areaServed": ["Tuscaloosa AL", "Northport AL", "Moundville AL", "West Alabama"],
        "hasMap": BUSINESS["maps"],
        "openingHoursSpecification": hours_spec,
        "sameAs": list(SOCIALS.values()),
        "foundingDate": BUSINESS["founded"],
        "paymentAccepted": "Cash, Credit Card, Apple Pay, Google Pay, Cash App",
        "currenciesAccepted": "USD",
    }

def ld_website():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": BUSINESS["name"],
        "url": SITE_BASE + "/",
        "publisher": {"@id": SITE_BASE + "/#store"},
    }

def ld_breadcrumbs(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
            for i, (n, u) in enumerate(items)
        ],
    }

def ld_itemlist(name, prods, page_url):
    els = []
    for i, p in enumerate(prods):
        item = {
            "@type": "Product",
            "name": p["name"],
            "url": PRODUCT_BASE + p["url"],
        }
        if p["image"]:
            item["image"] = p["image"] + "?width=900"
        if p["priceMin"] is not None:
            offer = {
                "@type": "Offer", "priceCurrency": "USD",
                "price": "%.2f" % p["priceMin"],
                "availability": "https://schema.org/InStock",
                "url": PRODUCT_BASE + p["url"],
                "seller": {"@id": SITE_BASE + "/#store"},
            }
            if p["priceMax"] and p["priceMax"] != p["priceMin"]:
                offer = {
                    "@type": "AggregateOffer", "priceCurrency": "USD",
                    "lowPrice": "%.2f" % p["priceMin"], "highPrice": "%.2f" % p["priceMax"],
                    "url": PRODUCT_BASE + p["url"],
                }
            item["offers"] = offer
        els.append({"@type": "ListItem", "position": i + 1, "item": item})
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": name,
        "url": page_url,
        "numberOfItems": len(prods),
        "itemListElement": els,
    }

FAQS = [
    ("Where is River's Edge Market located?",
     "River's Edge Market is an upscale boutique located at 1340 The Townes, Tuscaloosa, Alabama 35406. The shop was founded in Moundville in 2019 and now serves the greater Tuscaloosa and West Alabama area."),
    ("What are River's Edge Market's store hours?",
     "The boutique is open Tuesday through Friday from 10:00 AM to 5:00 PM and Saturday from 10:00 AM to 2:00 PM. The store is closed on Sunday and Monday."),
    ("What brands does River's Edge Market carry?",
     "River's Edge Market carries a curated mix of beloved brands including Capri Blue, NEST New York, Circle E Candles, ABLE leather goods, Bogg Bag, Swig Life, Pura Vida, NYDJ denim, 1818 Farms, Hello Mello loungewear, Pirani, Kanga Coolers, My Drink Bomb, and Riman skincare, alongside curated women's fashion and jewelry."),
    ("Can I shop River's Edge Market online?",
     "Yes. Every piece on this site can be purchased online through the boutique's secure Square checkout, with shipping available and complimentary shipping on orders over $150. Local pickup is also offered in Tuscaloosa."),
    ("Does River's Edge Market sell gift cards?",
     "Yes — digital gift cards are available in any amount and are delivered instantly by email, making them a perfect last-minute gift."),
    ("What kind of store is River's Edge Market?",
     "River's Edge Market is a locally owned boutique gift shop specializing in home decor, home fragrance, women's fashion and accessories, fine plated jewelry, ethically made leather goods, and gifts with an eclectic but refined flair."),
]

def ld_faq():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQS
        ],
    }

# ---------------------------------------------------------------- sections
def visit_section(with_head=True):
    headline = """
      <span class="eyebrow">Visit the boutique</span>
      <h2>In the heart of Tuscaloosa</h2>
      <p class="lede" style="margin-top:0.9rem;">Come experience the shop in person — new arrivals land weekly, and our team loves helping you find the perfect piece.</p>
    """ if with_head else ""
    return """
<section class="block" id="visit">
  <div class="wrap visit-grid">
    <div class="reveal">
      %(headline)s
      <ul class="contact-lines">
        <li><b>Address</b><span>%(street)s, %(city)s, %(region)s %(zip)s</span></li>
        <li><b>Phone</b><a href="tel:%(phone_e164)s">%(phone)s</a></li>
        <li><b>Email</b><a href="mailto:%(email)s">%(email)s</a></li>
      </ul>
      <div class="btn-row">
        <a class="btn btn-dark" href="%(maps)s" target="_blank" rel="noopener">Get Directions</a>
        <a class="btn btn-outline" href="tel:%(phone_e164)s">Call the Shop</a>
      </div>
    </div>
    <div class="reveal">
      <h3 style="margin-bottom:1rem;">Store Hours</h3>
      <table class="hours-table">%(hours)s</table>
    </div>
  </div>
</section>
""" % {"headline": headline, "hours": hours_rows(), "street": BUSINESS["street"],
       "city": BUSINESS["city"], "region": BUSINESS["region"], "zip": BUSINESS["zip"],
       "phone": BUSINESS["phone"], "phone_e164": BUSINESS["phone_e164"],
       "email": BUSINESS["email"], "maps": BUSINESS["maps"]}

def faq_section(items, title="Questions, answered"):
    lis = "".join(
        '<details class="faq-item"><summary>%s</summary><div class="faq-body"><p>%s</p></div></details>'
        % (esc(q), esc(a)) for q, a in items)
    return """
<section class="block" style="padding-top:0;">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">FAQ</span><h2>%s</h2></div>
      <a class="link-arrow" href="%sfaq.html">All questions</a>
    </div>
    <div class="faq-list reveal">%s</div>
  </div>
</section>
""" % (esc(title), rel(""), lis)

# ---------------------------------------------------------------- pages
CDN = "https://131443099.cdn6.editmysite.com/uploads/1/3/1/4/131443099/"

DEPT_TILE_IMG = {
    "Home Fragrance": CDN + "HS3VDPVCAUBNLPH57G34F6VV.jpeg",
    "Bath & Body": CDN + "RXNMKXKETUFRVYLZ3EHBFJHA.jpeg",
    "Jewelry": CDN + "TOYE6PHLUMVOQABI4LYSWJQ3.jpeg",
    "Bags & Leather": CDN + "ADKTPVHTMFQYZXWVQIEQLWSN.jpeg",
    "Drinkware & Entertaining": CDN + "4EC2MO3TWUUNTVGBYWE27BH2.jpeg",
    "Apparel": CDN + "CKW37XQA73DWNEHRPDC7BWQJ.jpeg",
    "Loungewear": CDN + "6XVTKM46YGKPQTOH73X6QLJY.png",
    "Baby & Kids": CDN + "IG6RVSGCSG4VR26G6JLZQQWT.png",
}

FEATURED_IDS = ["2600", "2496", "LGIHIQVZZ63HXCM2X753ZWJL", "2623",
                "2481", "2614", "2750", "2531"]

def dept_first_collection(dept):
    for slug, (name, d, blurb) in COLLECTIONS.items():
        if d == dept:
            return slug
    return None

def page_index():
    CTX["depth"] = 0
    feat = [BY_ID[i] for i in FEATURED_IDS if i in BY_ID]
    dept_cards = []
    counts = {}
    for p in PRODUCTS:
        counts[dept_of(p)] = counts.get(dept_of(p), 0) + 1
    for dept in DEPARTMENTS:
        slug = dept_first_collection(dept)
        dept_cards.append(
            '<a class="dept-card reveal" href="shop.html?dept=%s">'
            '<img src="%s?width=600" alt="%s at River\'s Edge Market" loading="lazy" decoding="async">'
            '<div class="dept-label"><b>%s</b><span>%d pieces</span></div></a>'
            % (dept.replace(" ", "%20").replace("&", "%26"), DEPT_TILE_IMG[dept], esc(dept), esc(dept), counts.get(dept, 0)))
    marq = "".join("<span>%s</span>" % esc(b) for b in BRANDS)
    body = header("home") + """
<main>
<section class="hero">
  <div class="wrap hero-inner">
    <div>
      <span class="eyebrow">Tuscaloosa&rsquo;s boutique destination</span>
      <h1>A finer way<br>to <em>shop.</em></h1>
      <p class="lede">Curated home d&eacute;cor, women&rsquo;s fashion, and gifts with an eclectic but refined flair — from the brands you love, gathered along the river&rsquo;s edge.</p>
      <div class="btn-row">
        <a class="btn btn-solid" href="shop.html">Shop the Collection</a>
        <a class="btn btn-ghost" href="#visit">Visit the Boutique</a>
      </div>
    </div>
    <div class="hero-collage">
      <figure><img src="%(hero1)s?width=900" alt="Champagne satin maxi dress from River's Edge Market" fetchpriority="high"></figure>
      <figure><img src="%(hero2)s?width=900" alt="ABLE leather classic tote in cognac" fetchpriority="high"></figure>
      <div class="hero-badge">Est. %(founded)s<br>West&nbsp;Alabama</div>
    </div>
  </div>
  <div class="marquee" aria-hidden="true"><div class="marquee-track">%(marq)s%(marq)s</div></div>
</section>

<section class="block">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">Shop by department</span><h2>Every corner, curated</h2></div>
      <a class="link-arrow" href="shop.html">Shop everything</a>
    </div>
    <div class="dept-grid">%(depts)s</div>
  </div>
</section>

<section class="block" style="padding-top:0;">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">New &amp; noteworthy</span><h2>Pieces we love right now</h2></div>
      <a class="link-arrow" href="shop.html">View all %(total)d</a>
    </div>
    <div class="product-grid reveal">%(featured)s</div>
  </div>
</section>

<section class="block" style="padding-top:0;">
  <div class="wrap">
    <div class="band reveal">
      <div>
        <span class="eyebrow">Our promise</span>
        <h2>Superior service, personalized attention</h2>
        <p style="margin-top:1rem;max-width:52ch;">From our founder to our front line, we put love and careful thought into everything we do — every collection hand-picked, every visit personal. Shop online with secure Square checkout, or come see us in Tuscaloosa.</p>
      </div>
      <div class="btn-row" style="justify-content:flex-end;">
        <a class="btn btn-solid" href="about.html">Our Story</a>
        <a class="btn btn-ghost" href="%(gift)s" target="_blank" rel="noopener">Give a Gift Card</a>
      </div>
    </div>
  </div>
</section>

%(visit)s

%(faq)s

<section class="block" style="padding-top:0;">
  <div class="wrap newsletter-box reveal">
    <span class="eyebrow" style="justify-content:center;">Stay in the loop</span>
    <h2>New arrivals, first looks, private sales</h2>
    <p class="lede" style="margin:1rem auto 1.6rem;">Follow along for weekly drops and boutique happenings.</p>
    <div class="btn-row" style="justify-content:center;">
      <a class="btn btn-dark" href="%(ig)s" target="_blank" rel="noopener">Follow on Instagram</a>
      <a class="btn btn-outline" href="mailto:%(email)s?subject=Add%%20me%%20to%%20the%%20list">Join the Email List</a>
    </div>
    %(socials)s
  </div>
</section>
</main>
""" % {"hero1": CDN + "CKW37XQA73DWNEHRPDC7BWQJ.jpeg", "hero2": CDN + "ADKTPVHTMFQYZXWVQIEQLWSN.jpeg",
       "founded": BUSINESS["founded"], "marq": marq, "depts": "".join(dept_cards),
       "featured": "".join(card(p) for p in feat), "total": len(PRODUCTS),
       "visit": visit_section(), "faq": faq_section(FAQS[:4]), "gift": GIFT_CARD_URL,
       "ig": SOCIALS["Instagram"], "email": BUSINESS["email"], "socials": socials_html()}
    return head(
        "River's Edge Market | Upscale Boutique in Tuscaloosa, AL — Home Decor, Fashion & Gifts",
        "River's Edge Market is Tuscaloosa's upscale boutique for home decor, candles, women's fashion, jewelry, and gifts. Shop Capri Blue, NEST, ABLE, Bogg, Swig & more — online or at 1340 The Townes.",
        "", [ld_store(), ld_website(), ld_faq()],
        ogimg=CDN + "CKW37XQA73DWNEHRPDC7BWQJ.jpeg?width=1200",
    ) + body + footer() + "</body></html>"

def shop_data_json():
    rows = []
    for p in PRODUCTS:
        rows.append({
            "n": p["name"], "u": PRODUCT_BASE + p["url"],
            "pm": p["priceMin"], "px": p["priceMax"],
            "i": p["image"], "c": primary_collection(p), "d": dept_of(p),
        })
    return json.dumps(rows, ensure_ascii=False)

def page_shop():
    CTX["depth"] = 0
    chips = ['<button class="chip active" data-dept="all">All</button>']
    for d in DEPARTMENTS:
        chips.append('<button class="chip" data-dept="%s">%s</button>' % (esc(d), esc(d)))
    body = header("shop") + """
<main>
<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a><span>/</span>Shop</div>
    <h1>Shop the Boutique</h1>
    <p class="lede">Every piece in the shop — %(total)d curated finds across home, fashion, and gifts. Checkout is handled securely by Square.</p>
  </div>
</section>
<section style="padding-bottom: clamp(3rem, 6vw, 5rem);">
  <div class="wrap">
    <div class="toolbar" role="group" aria-label="Filter products">
      %(chips)s
      <div class="search-box">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <input id="shop-search" type="search" placeholder="Search pieces or brands&hellip;" aria-label="Search products">
      </div>
    </div>
    <div class="result-count" id="result-count" aria-live="polite"></div>
    <div class="product-grid" id="shop-grid"></div>
  </div>
</section>
</main>
<script type="application/json" id="product-data">%(data)s</script>
""" % {"total": len(PRODUCTS), "chips": "".join(chips), "data": shop_data_json()}
    return head(
        "Shop All | River's Edge Market — Boutique Home Decor, Fashion & Gifts Online",
        "Browse all %d pieces at River's Edge Market: Capri Blue and Circle E candles, ABLE leather, Bogg Bags, Swig drinkware, women's fashion, jewelry & gifts. Free shipping over $150." % len(PRODUCTS),
        "shop.html",
        [ld_breadcrumbs([("Home", SITE_BASE + "/"), ("Shop", SITE_BASE + "/shop.html")])],
    ) + body + footer() + "</body></html>"

def page_collection(slug):
    CTX["depth"] = 1
    name, dept, blurb = COLLECTIONS[slug]
    prods = [p for p in PRODUCTS if slug in p["cats"]]
    if not prods:
        return None
    url = SITE_BASE + "/collections/%s.html" % slug
    hero_img = next((p["image"] for p in prods if p["image"]), None)
    body = header() + """
<main>
<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="../index.html">Home</a><span>/</span><a href="../shop.html">Shop</a><span>/</span>%(name)s</div>
    <h1>%(name)s</h1>
    <p class="lede">%(blurb)s</p>
  </div>
</section>
<section class="block">
  <div class="wrap">
    <div class="result-count">%(n)d pieces &middot; %(dept)s</div>
    <div class="product-grid">%(cards)s</div>
    <div class="btn-row" style="margin-top:2.6rem;">
      <a class="btn btn-dark" href="../shop.html">Shop Everything</a>
      <a class="btn btn-outline" href="../shop.html?dept=%(deptq)s">More %(dept)s</a>
    </div>
  </div>
</section>
</main>
""" % {"name": esc(name), "blurb": esc(blurb), "n": len(prods), "dept": esc(dept),
       "deptq": dept.replace(" ", "%20").replace("&", "%26"),
       "cards": "".join(card(p) for p in prods)}
    return head(
        "%s | River's Edge Market — Tuscaloosa, AL" % name,
        "%s Shop the %s collection at River's Edge Market — %d pieces with secure online checkout and free shipping over $150." % (blurb, name, len(prods)),
        "collections/%s.html" % slug,
        [ld_breadcrumbs([("Home", SITE_BASE + "/"), ("Shop", SITE_BASE + "/shop.html"), (name, url)]),
         ld_itemlist(name + " — River's Edge Market", prods, url)],
        ogimg=(hero_img + "?width=1200") if hero_img else None,
    ) + body + footer() + "</body></html>"

def page_about():
    CTX["depth"] = 0
    body = header("about") + """
<main>
<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a><span>/</span>Our Story</div>
    <h1>Rooted along the river&rsquo;s edge</h1>
    <p class="lede">Superior service, personalized attention — since %(founded)s.</p>
  </div>
</section>

<section class="block">
  <div class="wrap split">
    <div class="split-img reveal"><img src="%(img1)s?width=900" alt="Curated leather goods at River's Edge Market" loading="lazy"></div>
    <div class="reveal">
      <span class="eyebrow">Our story</span>
      <h2>A new kind of storefront</h2>
      <p class="lede" style="margin-top:1rem;">River&rsquo;s Edge Market began in %(founded)s in Moundville, Alabama, with a simple idea: bring the best from us to you. Today, from our home at The Townes in Tuscaloosa, we offer home d&eacute;cor, home accessories, women&rsquo;s fashion, fashion accessories, and gifts — every collection carrying an eclectic but refined flair, with charm that appeals to all.</p>
      <p class="lede" style="margin-top:1rem;">From our founder to our front-line team, we put love and careful thought into all we do. We hope you enjoy all we have to offer — and share the experience with others.</p>
      <div class="stat-row">
        <div class="stat"><b>%(founded)s</b><span>Founded</span></div>
        <div class="stat"><b>%(brands)d+</b><span>Curated brands</span></div>
        <div class="stat"><b>%(total)d</b><span>Pieces in shop</span></div>
      </div>
    </div>
  </div>
</section>

<section class="block" style="padding-top:0;">
  <div class="wrap">
    <div class="band reveal">
      <div>
        <span class="eyebrow">What we believe</span>
        <h2>Eclectic, but refined</h2>
        <p style="margin-top:1rem;max-width:56ch;">We choose every brand the way we&rsquo;d choose for our own homes — ethically made leather from ABLE, legendary Texas-poured Circle E candles, the iconic scents of Capri Blue and NEST New York, and fashion that feels as good as it looks.</p>
      </div>
      <div class="btn-row" style="justify-content:flex-end;">
        <a class="btn btn-solid" href="shop.html">Shop the Collection</a>
      </div>
    </div>
  </div>
</section>

%(visit)s
</main>
""" % {"founded": BUSINESS["founded"], "img1": CDN + "ADKTPVHTMFQYZXWVQIEQLWSN.jpeg",
       "brands": len(BRANDS), "total": len(PRODUCTS), "visit": visit_section()}
    return head(
        "Our Story | River's Edge Market — Boutique in Tuscaloosa, Alabama",
        "Founded in 2019 in Moundville and now home at The Townes in Tuscaloosa, River's Edge Market is a locally owned boutique for home decor, fashion, and gifts with an eclectic but refined flair.",
        "about.html",
        [ld_breadcrumbs([("Home", SITE_BASE + "/"), ("Our Story", SITE_BASE + "/about.html")]), ld_store()],
    ) + body + footer() + "</body></html>"

def page_contact():
    CTX["depth"] = 0
    body = header("contact") + """
<main>
<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a><span>/</span>Visit Us</div>
    <h1>Come say hello</h1>
    <p class="lede">Reach out and let us know if there is anything we can do for you — or better yet, come visit the boutique in person.</p>
  </div>
</section>

%(visit)s

<section class="block" style="padding-top:0;">
  <div class="wrap" style="max-width:720px;">
    <div class="reveal">
      <span class="eyebrow">Send a note</span>
      <h2>We&rsquo;d love to hear from you</h2>
      <p class="lede" style="margin:0.9rem 0 1.8rem;">Questions about a piece, a special order, or a gift? Drop us a line and we&rsquo;ll get right back to you.</p>
      <form class="form-grid" action="https://formsubmit.co/%(email)s" method="POST">
        <input type="hidden" name="_subject" value="New message from theriversedgemarket.com">
        <input type="hidden" name="_captcha" value="true">
        <input type="text" name="_honey" style="display:none">
        <div class="row2">
          <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" required autocomplete="name"></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
        </div>
        <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" rows="6" required></textarea></div>
        <div class="btn-row"><button class="btn btn-dark" type="submit">Send Message</button></div>
      </form>
    </div>
  </div>
</section>
</main>
""" % {"visit": visit_section(), "email": BUSINESS["email"]}
    return head(
        "Visit Us | River's Edge Market — 1340 The Townes, Tuscaloosa, AL",
        "Visit River's Edge Market at 1340 The Townes, Tuscaloosa, AL 35406. Open Tue–Fri 10–5, Sat 10–2. Call (659) 210-6590 or send us a message.",
        "contact.html",
        [ld_breadcrumbs([("Home", SITE_BASE + "/"), ("Visit Us", SITE_BASE + "/contact.html")]), ld_store()],
    ) + body + footer() + "</body></html>"

def page_faq():
    CTX["depth"] = 0
    lis = "".join(
        '<details class="faq-item"><summary>%s</summary><div class="faq-body"><p>%s</p></div></details>'
        % (esc(q), esc(a)) for q, a in FAQS)
    body = header() + """
<main>
<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a><span>/</span>FAQ</div>
    <h1>Frequently asked questions</h1>
    <p class="lede">Everything you need to know about shopping with River&rsquo;s Edge Market.</p>
  </div>
</section>
<section class="block">
  <div class="wrap">
    <div class="faq-list">%(faqs)s</div>
    <div class="btn-row" style="margin-top:2.4rem;">
      <a class="btn btn-dark" href="contact.html">Still have a question? Contact us</a>
    </div>
  </div>
</section>
</main>
""" % {"faqs": lis}
    return head(
        "FAQ | River's Edge Market — Hours, Location, Brands & Shipping",
        "Answers about River's Edge Market: location at The Townes in Tuscaloosa AL, store hours, the brands we carry, online ordering, shipping, and gift cards.",
        "faq.html",
        [ld_faq(), ld_breadcrumbs([("Home", SITE_BASE + "/"), ("FAQ", SITE_BASE + "/faq.html")])],
    ) + body + footer() + "</body></html>"

def page_404():
    CTX["depth"] = 0
    body = header() + """
<main>
<section class="block" style="text-align:center;padding-top:clamp(4rem,10vw,8rem);">
  <div class="wrap">
    <span class="eyebrow" style="justify-content:center;">404</span>
    <h1>This page drifted downstream</h1>
    <p class="lede" style="margin:1.2rem auto 2rem;">The page you&rsquo;re looking for doesn&rsquo;t exist — but the boutique is right this way.</p>
    <div class="btn-row" style="justify-content:center;">
      <a class="btn btn-dark" href="index.html">Back Home</a>
      <a class="btn btn-outline" href="shop.html">Shop the Collection</a>
    </div>
  </div>
</section>
</main>
"""
    return head("Page Not Found | River's Edge Market", "The page you're looking for could not be found.", "404.html") + body + footer() + "</body></html>"

# ---------------------------------------------------------------- static
PLACEHOLDER_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600">
<rect width="600" height="600" fill="#EFE9DE"/>
<circle cx="300" cy="272" r="104" fill="none" stroke="#AF8A55" stroke-width="2"/>
<text x="300" y="308" font-family="Georgia, serif" font-size="96" fill="#103A39" text-anchor="middle" font-style="italic">R</text>
<text x="300" y="430" font-family="Georgia, serif" font-size="24" fill="#47605D" text-anchor="middle" letter-spacing="6">RIVER'S EDGE MARKET</text>
</svg>"""

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="#103A39"/>
<text x="32" y="43" font-family="Georgia, serif" font-size="34" fill="#C9AE84" text-anchor="middle" font-style="italic">R</text>
</svg>"""

def build_sitemap(pages):
    today = datetime.date.today().isoformat()
    urls = []
    for path, prio in pages:
        urls.append("<url><loc>%s/%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (SITE_BASE, path, today, prio))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % "\n".join(urls)

ROBOTS = """User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE_BASE

def build_llms():
    lines = [
        "# River's Edge Market",
        "",
        "> River's Edge Market is an upscale, locally owned boutique at 1340 The Townes, Tuscaloosa, Alabama 35406, founded in 2019 in Moundville, AL. It sells home decor, home fragrance (Capri Blue, NEST New York, Circle E Candles), women's fashion and NYDJ denim, plated jewelry, Pura Vida jewelry, ABLE leather goods, Bogg Bags, Swig Life and Pirani drinkware, Hello Mello loungewear, 1818 Farms bath goods, and gifts. Orders check out securely through Square with free shipping over $150; local pickup is available.",
        "",
        "Hours: Tue-Fri 10:00-17:00, Sat 10:00-14:00, closed Sun-Mon.",
        "Phone: %s. Email: %s." % (BUSINESS["phone"], BUSINESS["email"]),
        "",
        "## Pages",
        "- [Shop all products](%s/shop.html): full catalog of %d products" % (SITE_BASE, len(PRODUCTS)),
        "- [Our story](%s/about.html): boutique history and mission" % SITE_BASE,
        "- [Visit / contact](%s/contact.html): address, hours, directions" % SITE_BASE,
        "- [FAQ](%s/faq.html): common questions" % SITE_BASE,
        "",
        "## Collections",
    ]
    for slug, (name, dept, blurb) in COLLECTIONS.items():
        n = sum(1 for p in PRODUCTS if slug in p["cats"])
        if n:
            lines.append("- [%s](%s/collections/%s.html): %s (%d products)" % (name, SITE_BASE, slug, blurb, n))
    return "\n".join(lines) + "\n"

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    os.makedirs(os.path.join(OUT, "collections"))

    shutil.copy(os.path.join(SRC, "styles.css"), os.path.join(OUT, "assets", "styles.css"))
    shutil.copy(os.path.join(SRC, "app.js"), os.path.join(OUT, "assets", "app.js"))
    with open(os.path.join(OUT, "assets", "placeholder.svg"), "w") as f:
        f.write(PLACEHOLDER_SVG)
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w") as f:
        f.write(FAVICON_SVG)

    pages = []  # (path, priority)

    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(page_index()); pages.append(("", "1.0"))
    with open(os.path.join(OUT, "shop.html"), "w") as f:
        f.write(page_shop()); pages.append(("shop.html", "0.9"))
    with open(os.path.join(OUT, "about.html"), "w") as f:
        f.write(page_about()); pages.append(("about.html", "0.7"))
    with open(os.path.join(OUT, "contact.html"), "w") as f:
        f.write(page_contact()); pages.append(("contact.html", "0.8"))
    with open(os.path.join(OUT, "faq.html"), "w") as f:
        f.write(page_faq()); pages.append(("faq.html", "0.7"))
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(page_404())

    made = 0
    for slug in COLLECTIONS:
        htmlpage = page_collection(slug)
        if htmlpage:
            with open(os.path.join(OUT, "collections", slug + ".html"), "w") as f:
                f.write(htmlpage)
            pages.append(("collections/%s.html" % slug, "0.8"))
            made += 1

    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(build_sitemap(pages))
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(ROBOTS)
    with open(os.path.join(OUT, "llms.txt"), "w") as f:
        f.write(build_llms())

    print("built: %d root pages + %d collection pages" % (6, made))

if __name__ == "__main__":
    main()
