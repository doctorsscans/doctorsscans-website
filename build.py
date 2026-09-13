#!/usr/bin/env python3
"""Builds the Doctors Scans static site into ./out"""
import os, shutil, html
from data import *

OUT = "out"

# ---------------------------------------------------------------- helpers
def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def wa_link(num, msg):
    from urllib.parse import quote
    return f"https://wa.me/{num}?text={quote(msg)}"

# ---------------------------------------------------------------- head
def head(title, desc, canonical, banner="banner-home", extra_schema=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM}');</script>
<!-- End Google Tag Manager -->

<title>{html.escape(html.unescape(title))}</title>
<meta name="description" content="{html.escape(html.unescape(desc))}">
<link rel="canonical" href="{SITE}{canonical}">
<meta name="google-site-verification" content="{GSV}">
<meta name="robots" content="index, follow">
<meta name="geo.region" content="IN-KL">
<meta name="geo.placename" content="Kollam, Kerala">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{html.escape(html.unescape(title))}">
<meta property="og:description" content="{html.escape(html.unescape(desc))}">
<meta property="og:url" content="{SITE}{canonical}">
<meta property="og:image" content="{SITE}/assets/images/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(html.unescape(title))}">
<meta name="twitter:description" content="{html.escape(html.unescape(desc))}">
<meta name="twitter:image" content="{SITE}/assets/images/og-image.jpg">

<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/images/icon-32.png">
<link rel="apple-touch-icon" href="/assets/images/icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#6DC9F0">

<link rel="stylesheet" href="/assets/vendor/bootstrap.min.css?v=2">
<link rel="stylesheet" href="/assets/css/main.css?v=2">
{extra_schema}
</head>
<body class="page-{banner}">
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" title="Google Tag Manager"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager -->
<a class="skip-link" href="#main">Skip to content</a>
"""

# ---------------------------------------------------------------- nav
def nav(active=""):
    items = [("/", "Home", "home"), ("/services/", "Services", "services"),
             ("/packages/", "Packages", "packages"), ("/doctors/", "Doctors", "doctors"),
             ("/branches/", "Branches", "branches"), ("/about/", "About Us", "about"),
             ("/contact/", "Contact", "contact")]
    li = ""
    for href, label, key in items:
        cur = ' aria-current="page"' if key == active else ""
        cls = "nav-link active" if key == active else "nav-link"
        li += f'<li class="nav-item"><a class="{cls}" href="{href}"{cur}>{label}</a></li>\n'
    return f"""<nav class="navbar navbar-expand-lg sticky-top" aria-label="Main navigation">
  <div class="container">
    <a class="navbar-brand" href="/">
      <img src="/assets/images/logo.webp" alt="" width="44" height="44" decoding="async">
      <span>Doctors Scans</span>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarNav" aria-controls="navbarNav"
            aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto align-items-lg-center">
        {li}
        <li class="nav-item ms-lg-3">
          <button type="button" class="btn btn-whatsapp btn-sm px-3" data-book="an appointment">
            <svg class="wa" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.24-8.23a8.2 8.2 0 0 1 8.23 8.24c0 4.54-3.69 8.23-8.22 8.23zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.13-.15.17-.25.25-.41.09-.17.04-.31-.02-.43-.06-.13-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.16 0-.43.06-.65.31-.23.25-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.21 3.72.59.25 1.05.4 1.4.52.59.19 1.13.16 1.55.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.29z"/></svg>
            Book on WhatsApp
          </button>
        </li>
      </ul>
    </div>
  </div>
</nav>
"""

# ---------------------------------------------------------------- footer
def footer():
    links = "".join(
        f'<li><a href="/branches/{b["slug"]}/">{b["name"]}</a></li>' for b in BRANCHES)
    quick = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in
                    [("/services/", "Services"), ("/packages/", "Health Packages"),
                     ("/doctors/", "Our Doctors"), ("/branches/", "All Branches"),
                     ("/about/", "About Us"), ("/contact/", "Contact")])
    main = BRANCHES[0]
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="row g-4">
      <div class="col-lg-4">
        <div class="footer-brand">
          <img src="/assets/images/logo.webp" alt="" width="48" height="48" loading="lazy" decoding="async">
          <div>
            <strong>Doctors Scans &amp; Labs</strong>
            <span>A unit of {LEGAL}</span>
          </div>
        </div>
        <p class="footer-note">Advanced diagnostic imaging and laboratory services across
        Kollam and Thiruvananthapuram districts.</p>
        <p class="footer-hours">{HOURS_WEEK}<br>{HOURS_SUN}</p>
      </div>
      <div class="col-6 col-lg-2">
        <h2 class="footer-head">Quick Links</h2>
        <ul class="footer-list">{quick}</ul>
      </div>
      <div class="col-6 col-lg-3">
        <h2 class="footer-head">Our Centres</h2>
        <ul class="footer-list">{links}</ul>
      </div>
      <div class="col-lg-3">
        <h2 class="footer-head">Get in Touch</h2>
        <p class="footer-list">
          <a href="tel:{main['phone']}">{main['display']}</a><br>
          <a href="tel:{main['landline']}">{main['landline_display']}</a>
        </p>
        <button type="button" class="btn btn-whatsapp btn-sm" data-book="an appointment">
          <svg class="wa" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.24-8.23a8.2 8.2 0 0 1 8.23 8.24c0 4.54-3.69 8.23-8.22 8.23zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.13-.15.17-.25.25-.41.09-.17.04-.31-.02-.43-.06-.13-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.16 0-.43.06-.65.31-.23.25-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.21 3.72.59.25 1.05.4 1.4.52.59.19 1.13.16 1.55.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.29z"/></svg>
          Book on WhatsApp
        </button>
        <p class="footer-social">
          <a href="{INSTAGRAM}" rel="noopener" aria-label="Doctors Scans on Instagram">
            <svg viewBox="0 0 24 24" aria-hidden="true" width="26" height="26"><path d="M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558.788-.306 1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06zm0 3.678a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm7.846-10.405a1.441 1.441 0 01-2.88 0 1.44 1.44 0 012.88 0z"/></svg>
          </a>
        </p>
      </div>
    </div>
    <hr>
    <p class="footer-legal">&copy; 2026 {LEGAL}. All rights reserved.</p>
  </div>
</footer>

<div class="modal fade" id="branchPicker" tabindex="-1" aria-labelledby="branchPickerLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title h5" id="branchPickerLabel">Which centre would you like?</h2>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p class="picker-intro">Choose your nearest centre. We will open WhatsApp with your
        message ready to send.</p>
        <div class="picker-list">
          {"".join(f'''<a class="picker-item" href="#" data-wa="{b['wa']}" data-slug="{b['slug']}">
            <span class="picker-name">{b['name']}</span>
            <span class="picker-sub">{b['landmark']}</span>
            <span class="picker-num">{b['display']}</span>
          </a>''' for b in BRANCHES)}
        </div>
      </div>
    </div>
  </div>
</div>

<a class="wa-float" href="#" data-book="an appointment" aria-label="Book on WhatsApp">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.24-8.23a8.2 8.2 0 0 1 8.23 8.24c0 4.54-3.69 8.23-8.22 8.23zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.13-.15.17-.25.25-.41.09-.17.04-.31-.02-.43-.06-.13-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.16 0-.43.06-.65.31-.23.25-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.21 3.72.59.25 1.05.4 1.4.52.59.19 1.13.16 1.55.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.29z"/></svg>
</a>

<script src="/assets/vendor/bootstrap.bundle.min.js?v=2" defer></script>
<script src="/assets/js/main.js?v=2" defer></script>
</body>
</html>
"""

def hero(cls, h1, sub, extra=""):
    return f"""<header class="hero {cls}">
  <div class="container">
    <h1>{h1}</h1>
    <p class="hero-sub">{sub}</p>
    {extra}
  </div>
</header>
"""

def wa_btn(service, cls="btn btn-whatsapp w-100", at=None):
    scope = f' data-at="{",".join(at)}"' if at else ""
    return f"""<button type="button" class="{cls}" data-book="{html.escape(service)}"{scope}>
<svg class="wa" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.24-8.23a8.2 8.2 0 0 1 8.23 8.24c0 4.54-3.69 8.23-8.22 8.23zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.13-.15.17-.25.25-.41.09-.17.04-.31-.02-.43-.06-.13-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.16 0-.43.06-.65.31-.23.25-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.21 3.72.59.25 1.05.4 1.4.52.59.19 1.13.16 1.55.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.29z"/></svg>
Book on WhatsApp</button>"""

def crumbs(trail):
    """trail = [(url,label), ...] last item is current page"""
    items, ld = [], []
    for i, (url, label) in enumerate(trail):
        last = i == len(trail) - 1
        items.append(f'<li class="breadcrumb-item active" aria-current="page">{label}</li>'
                     if last else f'<li class="breadcrumb-item"><a href="{url}">{label}</a></li>')
        ld.append(f'{{"@type":"ListItem","position":{i+1},"name":"{label}","item":"{SITE}{url}"}}')
    return (f'<nav aria-label="Breadcrumb" class="crumbs"><div class="container">'
            f'<ol class="breadcrumb mb-0">{"".join(items)}</ol></div></nav>',
            f'<script type="application/ld+json">{{"@context":"https://schema.org",'
            f'"@type":"BreadcrumbList","itemListElement":[{",".join(ld)}]}}</script>')

# ---------------------------------------------------------------- schema
def branch_schema(b, service_list=False):
    svc = ""
    if service_list:
        svc = ',"availableService":[' + ",".join(
            f'{{"@type":"MedicalTest","name":"{s["name"]}"}}' for s in services_for(b)) + "]"
    tel = f'"{b["phone"]}"'
    return f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"DiagnosticLab",
"@id":"{SITE}/branches/{b['slug']}/#business",
"name":"Doctors Scans & Labs, {b['name']}",
"parentOrganization":{{"@type":"Organization","name":"{LEGAL}","url":"{SITE}/"}},
"url":"{SITE}/branches/{b['slug']}/",
"image":"{SITE}/assets/images/og-image.jpg",
"logo":"{SITE}/assets/images/logo.jpg",
"telephone":{tel},
"address":{{"@type":"PostalAddress","streetAddress":"{b['address']}",
"addressLocality":"{b['locality']}","addressRegion":"{b['region']}",
"postalCode":"{b['postal']}","addressCountry":"IN"}},
"geo":{{"@type":"GeoCoordinates","latitude":{b['lat']},"longitude":{b['lng']}}},
"hasMap":"{b['map']}",
"openingHoursSpecification":[
{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"09:00","closes":"19:30"}},
{{"@type":"OpeningHoursSpecification","dayOfWeek":"Sunday","opens":"09:00","closes":"13:00"}}],
"sameAs":["{INSTAGRAM}"]{svc}}}
</script>"""

ORG_SCHEMA = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"MedicalOrganization",
"@id":"{SITE}/#organization","name":"{BRAND}","legalName":"{LEGAL}",
"url":"{SITE}/","logo":"{SITE}/assets/images/logo.jpg",
"image":"{SITE}/assets/images/og-image.jpg",
"telephone":"{BRANCHES[0]['phone']}","sameAs":["{INSTAGRAM}"],
"department":[{",".join(f'{{"@id":"{SITE}/branches/{b["slug"]}/#business"}}' for b in BRANCHES)}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebSite","url":"{SITE}/","name":"{BRAND}"}}
</script>"""

# ================================================================ PAGES
def build_home():
    cards = ""
    for s in SERVICES:
        cards += f"""<div class="col-md-6 col-lg-4">
  <article class="card svc-card h-100">
    <img src="/assets/images/{s['img']}.webp" class="card-img-top" alt="{s['name']}"
         width="1200" height="800" loading="lazy" decoding="async">
    <div class="card-body d-flex flex-column">
      <h3 class="card-title">{s['name']}</h3>
      {'<p class="only-at">Available at Parippally</p>' if len(s['at']) < len(BRANCHES) else ''}
      <p class="card-text flex-grow-1">{s['short']}</p>
      <div class="mt-auto d-grid gap-2">
        <a href="/services/{s['slug']}/" class="btn btn-outline-brand">Read more</a>
        {wa_btn(s['name'], at=s['at'])}
      </div>
    </div>
  </article>
</div>
"""
    pkg = ""
    for p in PACKAGES:
        pkg += f"""<div class="col-md-6 col-lg-4">
  <article class="card pkg-card h-100 text-center">
    <img src="/assets/images/{p['img']}.webp" class="card-img-top" alt="{p['name']}"
         width="1000" height="667" loading="lazy" decoding="async">
    <div class="card-body d-flex flex-column">
      <h3 class="card-title">{p['name']}</h3>
      <p class="card-text flex-grow-1">{p['short']}</p>
      <div class="mt-auto">{wa_btn(p['name'] + " (health package)")}</div>
    </div>
  </article>
</div>
"""
    docs = "".join(f"""<div class="col-6 col-md-4 col-lg-3">
  <article class="doctor-card h-100">
    <img src="/assets/images/doctor-placeholder.webp" alt="{d['name']}"
         width="500" height="500" loading="lazy" decoding="async">
    <h3 class="doctor-name">{d['name']}</h3>
    <p class="doctor-qual">{d['qual']}</p>
    <p class="doctor-role">{d['role']}</p>
  </article>
</div>""" for d in DOCTORS)

    branch_strip = "".join(f"""<a class="branch-chip" href="/branches/{b['slug']}/">
      <strong>{b['name']}</strong><span>{b['display']}</span></a>""" for b in BRANCHES)

    title = "Doctors Scans &amp; Labs | Diagnostic Centre in Parippally, Kollam"
    desc = ("Ultrasound, fetal medicine, Doppler, echo, FibroScan, PFT and laboratory "
            "services at six centres across Kollam and Thiruvananthapuram. Open 9 AM to 7:30 PM.")
    h = head(title, desc, "/", "banner-home", ORG_SCHEMA)
    body = f"""{nav('home')}
<main id="main">
{hero('hero-home', 'Doctors Scans &amp; Labs',
      'Advanced diagnostic imaging and laboratory services, close to home.',
      f'''<p class="hero-meta">A unit of {LEGAL}</p>
      <div class="hero-branches">{branch_strip}</div>
      <p class="hero-hours">Open {HOURS_WEEK} &nbsp;&middot;&nbsp; {HOURS_SUN}</p>
      <div class="hero-cta">{wa_btn("an appointment", "btn btn-whatsapp btn-lg")}
      <a href="tel:{BRANCHES[0]['phone']}" class="btn btn-outline-light btn-lg">Call {BRANCHES[0]['display']}</a></div>''')}

<section class="section" id="services">
  <div class="container">
    <h2 class="section-title">Services we provide</h2>
    <p class="section-lede">Imaging, fetal medicine and laboratory testing, reported by
    consultant radiologists.</p>
    <div class="row g-4">{cards}</div>
  </div>
</section>

<section class="section section-alt" id="packages">
  <div class="container">
    <h2 class="section-title">Health checkup packages</h2>
    <p class="section-lede">Message us on WhatsApp for current pricing and what each package
    includes at your nearest centre.</p>
    <div class="row g-4">{pkg}</div>
  </div>
</section>

<section class="section" id="doctors">
  <div class="container">
    <h2 class="section-title">Our doctors</h2>
    <div class="row g-4 justify-content-center">{docs}</div>
  </div>
</section>

<section class="section section-alt" id="branches">
  <div class="container">
    <h2 class="section-title">Six centres across Kollam &amp; Thiruvananthapuram</h2>
    <div class="row g-3">
      {"".join(f'''<div class="col-md-6 col-lg-4">
        <a class="branch-tile" href="/branches/{b['slug']}/">
          <h3>{b['name']}</h3>
          <p>{b['landmark']}</p>
          <span class="branch-tel">{b['display']}</span>
        </a></div>''' for b in BRANCHES)}
    </div>
  </div>
</section>
</main>
{footer()}"""
    write("index.html", h + body)

def build_services_index():
    cards = "".join(f"""<div class="col-md-6 col-lg-4">
  <article class="card svc-card h-100">
    <img src="/assets/images/{s['img']}.webp" class="card-img-top" alt="{s['name']}"
         width="1200" height="800" loading="lazy" decoding="async">
    <div class="card-body d-flex flex-column">
      <h2 class="card-title h5">{s['name']}</h2>
      {'<p class="only-at">Available at Parippally</p>' if len(s['at']) < len(BRANCHES) else ''}
      <p class="card-text flex-grow-1">{s['short']}</p>
      <div class="mt-auto d-grid gap-2">
        <a href="/services/{s['slug']}/" class="btn btn-outline-brand">Read more</a>
        {wa_btn(s['name'], at=s['at'])}
      </div>
    </div>
  </article>
</div>""" for s in SERVICES)
    cb, cbld = crumbs([("/", "Home"), ("/services/", "Services")])
    title = "Diagnostic Services | Doctors Scans &amp; Labs, Kollam"
    desc = ("Ultrasound, fetal medicine, Doppler, echocardiography, FibroScan, pulmonary "
            "function testing, endoscopy and laboratory services across six centres.")
    write("services/index.html", head(title, desc, "/services/", "banner-services", cbld) +
          nav('services') + '<main id="main">' +
          hero('hero-services', 'Our services',
               f'{len(SERVICES)} diagnostic services across our six centres.') + cb + f"""
<section class="section"><div class="container"><div class="row g-4">{cards}</div></div></section>
</main>""" + footer())

def build_service_pages():
    for i, s in enumerate(SERVICES):
        others = "".join(
            f'<a class="rel-chip" href="/services/{o["slug"]}/">{o["name"]}</a>'
            for o in SERVICES if o["slug"] != s["slug"])
        pts = "".join(f"<li>{p}</li>" for p in s["points"])
        cb, cbld = crumbs([("/", "Home"), ("/services/", "Services"),
                           (f"/services/{s['slug']}/", s["name"])])
        _at = branches_for(s)
        note = ("Opens WhatsApp for our " + _at[0]["name"] + " centre with your message ready "
                "to send.") if len(_at) == 1 else ("Choose your nearest centre and we will open "
                "WhatsApp with your message ready to send.")
        schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"MedicalTest","name":"{s['name']}",
"description":"{html.escape(s['desc'])}","url":"{SITE}/services/{s['slug']}/",
"provider":{{"@id":"{SITE}/#organization"}}}}
</script>""" + cbld
        title = f"{s['name']} | Doctors Scans &amp; Labs, Kollam"
        at = branches_for(s)
        avail = "".join(f'<a class="branch-chip sm" href="/branches/{b["slug"]}/">{b["name"]}</a>'
                        for b in at)
        if len(at) < len(BRANCHES):
            names = " and ".join([", ".join(b["name"] for b in at[:-1]), at[-1]["name"]]) \
                    if len(at) > 1 else at[0]["name"]
            avail = (f'<p class="avail-note">This service is available at our {names} '
                     f'{"centres" if len(at) > 1 else "centre"} only.</p>') + avail
        write(f"services/{s['slug']}/index.html",
              head(title, s["desc"], f"/services/{s['slug']}/", "banner-services", schema) +
              nav('services') + '<main id="main">' +
              hero('hero-services', s["name"], s["short"]) + cb + f"""
<section class="section">
  <div class="container">
    <div class="row g-5 align-items-start">
      <div class="col-lg-6">
        <img src="/assets/images/{s['img']}.webp" alt="{s['name']}" class="svc-hero-img"
             width="1200" height="800" decoding="async">
      </div>
      <div class="col-lg-6">
        <h2>About this test</h2>
        <p class="lede">{s['long']}</p>
        <h3>What it covers</h3>
        <ul class="tick-list">{pts}</ul>
        <div class="svc-book">
          {wa_btn(s['name'], "btn btn-whatsapp btn-lg", at=s['at'])}
          <p class="svc-book-note">{note}</p>
        </div>
        <h3>Available at</h3>
        <div class="chip-row">{avail}</div>
      </div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">Other services</h2>
    <div class="chip-row">{others}</div>
  </div>
</section>
</main>""" + footer())

def build_packages():
    cards = "".join(f"""<div class="col-md-6 col-lg-4">
  <article class="card pkg-card h-100 text-center">
    <img src="/assets/images/{p['img']}.webp" class="card-img-top" alt="{p['name']}"
         width="1000" height="667" loading="lazy" decoding="async">
    <div class="card-body d-flex flex-column">
      <h2 class="card-title h5">{p['name']}</h2>
      <p class="card-text flex-grow-1">{p['short']}</p>
      <div class="mt-auto">{wa_btn(p['name'] + " (health package)")}</div>
    </div>
  </article>
</div>""" for p in PACKAGES)
    cb, cbld = crumbs([("/", "Home"), ("/packages/", "Health Packages")])
    title = "Health Checkup Packages | Doctors Scans &amp; Labs"
    desc = ("Master health checkup, diabetic, women's wellness, cardiac, executive and senior "
            "citizen packages. Message us on WhatsApp for pricing at your nearest centre.")
    write("packages/index.html", head(title, desc, "/packages/", "banner-packages", cbld) +
          nav('packages') + '<main id="main">' +
          hero('hero-packages', 'Health checkup packages',
               'Preventive screening bundles for every stage of life.') + cb + f"""
<section class="section"><div class="container">
  <p class="section-lede text-center">Package contents may vary slightly by centre. Message us
  on WhatsApp and we will send you current pricing and the full test list.</p>
  <div class="row g-4">{cards}</div>
</div></section>
</main>""" + footer())

def build_doctors():
    docs = "".join(f"""<div class="col-6 col-md-4 col-lg-3">
  <article class="doctor-card h-100">
    <img src="/assets/images/doctor-placeholder.webp" alt="{d['name']}"
         width="500" height="500" loading="lazy" decoding="async">
    <h2 class="doctor-name h5">{d['name']}</h2>
    <p class="doctor-qual">{d['qual']}</p>
    <p class="doctor-role">{d['role']}</p>
  </article>
</div>""" for d in DOCTORS)
    ld = ",".join(f'{{"@type":"Physician","name":"{d["name"]}","medicalSpecialty":"Radiology"}}'
                  for d in DOCTORS)
    cb, cbld = crumbs([("/", "Home"), ("/doctors/", "Doctors")])
    schema = (f'<script type="application/ld+json">{{"@context":"https://schema.org",'
              f'"@type":"ItemList","itemListElement":[{ld}]}}</script>' + cbld)
    title = "Our Doctors | Doctors Scans &amp; Labs, Kollam"
    desc = ("Meet the consultant radiologists at Doctors Scans & Labs, including specialists "
            "certified in fetal imaging and advanced cardiac imaging.")
    write("doctors/index.html", head(title, desc, "/doctors/", "banner-doctors", schema) +
          nav('doctors') + '<main id="main">' +
          hero('hero-doctors', 'Our doctors',
               'Every scan is reported by a consultant radiologist.') + cb + f"""
<section class="section"><div class="container">
  <div class="row g-4 justify-content-center">{docs}</div>
</div></section>
</main>""" + footer())

def build_about():
    cb, cbld = crumbs([("/", "Home"), ("/about/", "About Us")])
    title = "About Us | Doctors Scans &amp; Labs"
    desc = ("Doctors Scans & Labs is a diagnostic imaging and laboratory network with six "
            "centres across Kollam and Thiruvananthapuram districts in Kerala.")
    svc_line = ", ".join(s["name"] for s in SERVICES[:-1]) + " and " + SERVICES[-1]["name"]
    write("about/index.html", head(title, desc, "/about/", "banner-about", cbld) +
          nav('about') + '<main id="main">' +
          hero('hero-about', 'About us', 'Your health, our lifelong commitment.') + cb + f"""
<section class="section">
  <div class="container narrow">
    <h2>Who we are</h2>
    <p class="lede">Doctors Scans &amp; Labs is a diagnostic imaging and laboratory network
    operating six centres across Kollam and Thiruvananthapuram districts. We are a unit of
    {LEGAL}.</p>

    <p>Our main centre sits fifty metres from Paripally Government Medical College, and we have
    since grown to Kadakkal, Chirayinkeezhu, Kottarakkara, Karunagappalli and Kottiyam. Each
    centre is placed close to a government or taluk hospital, so that patients who need a scan
    or a test do not have to travel far to get one.</p>

    <h2>What we offer</h2>
    <p>Our services cover {svc_line}. CT scanning is available at our Parippally centre.
    Every scan is reported by a consultant radiologist, and
    our fetal medicine work is led by a radiologist with dedicated certification in fetal and
    advanced cardiac imaging.</p>

    <h2>How we work</h2>
    <p>A scan can be an anxious thing to wait for. Our staff are trained to explain what is
    about to happen, answer questions in plain language, and keep reporting times short so
    that you are not left waiting longer than necessary.</p>

    <p>We are open {HOURS_WEEK.lower()} and {HOURS_SUN.lower()}. Appointments can be made
    directly on WhatsApp with the centre nearest you.</p>

    <div class="cta-band">
      <h2>Book at your nearest centre</h2>
      <p>Pick a centre and message us on WhatsApp.</p>
      {wa_btn("an appointment", "btn btn-whatsapp btn-lg")}
    </div>
  </div>
</section>
</main>""" + footer())

def build_branches_index():
    cards = "".join(f"""<div class="col-md-6">
  <article class="branch-card h-100">
    <h2 class="branch-title h5">{b['name']}</h2>
    <p class="branch-addr">{b['address']}<br>{b['locality']}, {b['region']} {b['postal']}</p>
    <p class="branch-contact">
      <a href="tel:{b['phone']}">{b['display']}</a>
      {f"<br><a href='tel:{b['landline']}'>{b['landline_display']}</a>" if b['landline'] else ""}
    </p>
    <div class="branch-actions">
      <a class="btn btn-whatsapp btn-sm" href="{wa_link(b['wa'], f"Hello Doctors Scans {b['name']}, I would like to book an appointment.")}" rel="noopener">WhatsApp this centre</a>
      <a class="btn btn-outline-brand btn-sm" href="{b['map']}" rel="noopener">Directions</a>
      <a class="btn btn-link btn-sm" href="/branches/{b['slug']}/">Centre details</a>
    </div>
  </article>
</div>""" for b in BRANCHES)
    cb, cbld = crumbs([("/", "Home"), ("/branches/", "Branches")])
    title = "Our Branches | Doctors Scans &amp; Labs"
    desc = ("Six Doctors Scans & Labs centres: Parippally, Kadakkal, Chirayinkeezhu, "
            "Kottarakkara, Karunagappalli and Kottiyam. Addresses, phone numbers and directions.")
    write("branches/index.html", head(title, desc, "/branches/", "banner-contact", cbld) +
          nav('branches') + '<main id="main">' +
          hero('hero-contact', 'Our branches',
               'Six centres across Kollam and Thiruvananthapuram districts.') + cb + f"""
<section class="section"><div class="container"><div class="row g-4">{cards}</div></div></section>
</main>""" + footer())

def build_branch_pages():
    for b in BRANCHES:
        cb, cbld = crumbs([("/", "Home"), ("/branches/", "Branches"),
                           (f"/branches/{b['slug']}/", b["name"])])
        schema = branch_schema(b, service_list=True) + cbld
        title = (f"Scan Centre in {b['name']} | Doctors Scans &amp; Labs")
        desc = (f"Scan centre and diagnostic lab at {b['landmark']}. Ultrasound, Doppler, "
                f"echo and lab tests. Call {b['display']}.")
        svc = "".join(f'<a class="rel-chip" href="/services/{s["slug"]}/">{s["name"]}</a>'
                      for s in services_for(b))
        others = "".join(f'<a class="branch-chip sm" href="/branches/{o["slug"]}/">{o["name"]}</a>'
                         for o in BRANCHES if o["slug"] != b["slug"])
        landline = (f'<p class="ct-row"><span>Landline</span>'
                    f'<a href="tel:{b["landline"]}">{b["landline_display"]}</a></p>'
                    if b["landline"] else "")
        write(f"branches/{b['slug']}/index.html",
              head(title, desc, f"/branches/{b['slug']}/", "banner-contact", schema) +
              nav('branches') + '<main id="main">' +
              hero('hero-contact', f"Doctors Scans &amp; Labs, {b['name']}", b["landmark"]) + cb + f"""
<section class="section">
  <div class="container">
    <div class="row g-5">
      <div class="col-lg-5">
        <h2>Contact this centre</h2>
        <p class="lede">{b['blurb']}</p>
        <div class="contact-block">
          <p class="ct-row"><span>Address</span>{b['address']}, {b['locality']},
             {b['region']} {b['postal']}</p>
          <p class="ct-row"><span>Phone</span>
             <a href="tel:{b['phone']}">{b['display']}</a></p>
          {landline}
          <p class="ct-row"><span>Hours</span>{HOURS_WEEK}<br>{HOURS_SUN}</p>
        </div>
        <div class="d-grid gap-2 mt-4">
          <a class="btn btn-whatsapp btn-lg" rel="noopener"
             href="{wa_link(b['wa'], f"Hello Doctors Scans {b['name']}, I would like to book an appointment.")}">
            Message {b['name']} on WhatsApp</a>
          <a class="btn btn-outline-brand btn-lg" href="tel:{b['phone']}">Call {b['display']}</a>
          <a class="btn btn-link" href="{b['map']}" rel="noopener">Open in Google Maps</a>
        </div>
      </div>
      <div class="col-lg-7">
        <div class="branch-map">
          <iframe src="{b['embed']}" title="Map showing Doctors Scans &amp; Labs, {b['name']}"
                  loading="lazy" referrerpolicy="no-referrer-when-downgrade"
                  allowfullscreen></iframe>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">Services at this centre</h2>
    <div class="chip-row">{svc}</div>
    <h2 class="section-title mt-5">Our other centres</h2>
    <div class="chip-row">{others}</div>
  </div>
</section>
</main>""" + footer())

def build_contact():
    cb, cbld = crumbs([("/", "Home"), ("/contact/", "Contact")])
    b = BRANCHES[0]
    cards = "".join(f"""<div class="col-md-6 col-lg-4">
  <article class="branch-card h-100">
    <h2 class="branch-title h6">{x['name']}</h2>
    <p class="branch-addr">{x['landmark']}</p>
    <p class="branch-contact"><a href="tel:{x['phone']}">{x['display']}</a></p>
    <div class="branch-actions">
      <a class="btn btn-whatsapp btn-sm" rel="noopener"
         href="{wa_link(x['wa'], f"Hello Doctors Scans {x['name']}, I would like to book an appointment.")}">WhatsApp</a>
      <a class="btn btn-outline-brand btn-sm" href="{x['map']}" rel="noopener">Map</a>
      <a class="btn btn-link btn-sm" href="/branches/{x['slug']}/">Details</a>
    </div>
  </article>
</div>""" for x in BRANCHES)
    title = "Contact Us | Doctors Scans &amp; Labs, Kollam"
    desc = ("Call or WhatsApp any of our six centres across Kollam and Thiruvananthapuram. "
            "Open 9 AM to 7:30 PM Monday to Saturday, 9 AM to 1 PM Sunday.")
    write("contact/index.html", head(title, desc, "/contact/", "banner-contact",
                                     branch_schema(b) + cbld) +
          nav('contact') + '<main id="main">' +
          hero('hero-contact', 'Contact us',
               'Message the centre nearest you and we will take it from there.') + cb + f"""
<section class="section">
  <div class="container">
    <div class="row g-4 info-row">
      <div class="col-md-4"><div class="info-box">
        <h2 class="h6">Opening hours</h2>
        <p>{HOURS_WEEK}<br>{HOURS_SUN}</p></div></div>
      <div class="col-md-4"><div class="info-box">
        <h2 class="h6">Main centre</h2>
        <p>{b['landmark']}<br><a href="tel:{b['phone']}">{b['display']}</a></p></div></div>
      <div class="col-md-4"><div class="info-box">
        <h2 class="h6">Book a scan</h2>
        <p>Pick your centre below and message us on WhatsApp.</p></div></div>
    </div>
    <h2 class="section-title mt-5">All six centres</h2>
    <div class="row g-4">{cards}</div>
  </div>
</section>
</main>""" + footer())

OLD_URLS = {
    "/services/ultrasonography (usg)":         "/services/ultrasonography-usg/",
    "/services/advanced fetal medicine":       "/services/advanced-fetal-medicine/",
    "/services/usg guided procedures":         "/services/usg-guided-procedures/",
    "/services/fibroscan & elastography":      "/services/fibroscan-elastography/",
    "/services/doppler studies":               "/services/doppler-studies/",
    "/services/echocardiography (echo)":       "/services/echocardiography/",
    "/services/laboratory services":           "/services/laboratory-services/",
    "/services/pulmonary function test (pft)": "/services/pulmonary-function-test/",
    "/services/colonoscopy & endoscopy":       "/services/colonoscopy-endoscopy/",
    "/services/fetal interventions":           "/services/fetal-interventions/",
    "/header.html": "/", "/footer.html": "/",
}

def build_404():
    import json as _json
    table = _json.dumps(OLD_URLS, indent=2)
    redirect_js = rf"""<script>
/* Old site URLs used capital letters and spaces, e.g.
   /Services/Doppler%20Studies/ . Static hosts cannot 301 those, so this page
   catches them and forwards to the new address. Everything else shows the
   normal "page not found" content below. */
(function () {{
  var MOVED = {table};
  var p = decodeURIComponent(location.pathname).toLowerCase().replace(/\/+$/, "");
  if (MOVED[p]) {{ location.replace(MOVED[p]); return; }}
  /* Any other /Services/... link goes to the services index rather than a dead end. */
  if (p.indexOf("/services") === 0) {{ location.replace("/services/"); return; }}
  var simple = {{"/packages": "/packages/", "/doctors": "/doctors/",
                "/about": "/about/", "/contact": "/contact/"}};
  if (simple[p]) {{ location.replace(simple[p]); }}
}})();
</script>"""
    write("404.html", head("Page not found | Doctors Scans &amp; Labs",
                          "The page you were looking for could not be found.", "/404.html",
                          extra_schema=redirect_js) +
          nav() + '<main id="main">' + f"""
<section class="section"><div class="container narrow text-center py-5">
  <h1>We could not find that page</h1>
  <p class="lede">The link may be out of date. Here is where you can go instead.</p>
  <div class="chip-row justify-content-center mt-4">
    <a class="rel-chip" href="/">Home</a>
    <a class="rel-chip" href="/services/">Services</a>
    <a class="rel-chip" href="/packages/">Health packages</a>
    <a class="rel-chip" href="/branches/">Our branches</a>
    <a class="rel-chip" href="/contact/">Contact</a>
  </div>
</div></section>
</main>""" + footer())

# ---------------------------------------------------------------- support files
def build_support():
    urls = ["/", "/services/", "/packages/", "/doctors/", "/branches/", "/about/", "/contact/"]
    urls += [f"/services/{s['slug']}/" for s in SERVICES]
    urls += [f"/branches/{b['slug']}/" for b in BRANCHES]
    pri = {"/": "1.0", "/services/": "0.9", "/branches/": "0.9", "/contact/": "0.8"}
    entries = "".join(
        f"  <url><loc>{SITE}{u}</loc><changefreq>monthly</changefreq>"
        f"<priority>{pri.get(u, '0.7')}</priority></url>\n" for u in urls)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f'{entries}</urlset>\n')

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

    # old -> new redirects
    R = [("/Services/Ultrasonography%20(USG)/", "/services/ultrasonography-usg/"),
         ("/Services/Advanced%20Fetal%20Medicine/", "/services/advanced-fetal-medicine/"),
         ("/Services/USG%20Guided%20Procedures/", "/services/usg-guided-procedures/"),
         ("/Services/FibroScan%20&%20Elastography/", "/services/fibroscan-elastography/"),
         ("/Services/Doppler%20Studies/", "/services/doppler-studies/"),
         ("/Services/Echocardiography%20(Echo)/", "/services/echocardiography/"),
         ("/Services/Laboratory%20Services/", "/services/laboratory-services/"),
         ("/Services/Pulmonary%20Function%20Test%20(PFT)/", "/services/pulmonary-function-test/"),
         ("/Services/Colonoscopy%20&%20Endoscopy/", "/services/colonoscopy-endoscopy/"),
         ("/Services/Fetal%20Interventions/", "/services/fetal-interventions/"),
         ("/Services/", "/services/"), ("/Packages/", "/packages/"),
         ("/Doctors/", "/doctors/"), ("/About/", "/about/"), ("/Contact/", "/contact/")]

    write("_redirects", "".join(f"{a}  {b}  301\n" for a, b in R) +
          "/header.html  /  301\n/footer.html  /  301\n")

    ht = """# ---- Doctors Scans .htaccess (Apache / cPanel hosting) ----
Options -Indexes
DirectoryIndex index.html

RewriteEngine On

# Force HTTPS
RewriteCond %{HTTPS} !=on
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]

# Force www
RewriteCond %{HTTP_HOST} ^doctorsscans\\.com [NC]
RewriteRule ^(.*)$ https://www.doctorsscans.com/$1 [R=301,L]

# Old URLs -> new URLs
"""
    for a, b in R:
        src = a.strip("/").replace("%20", " ").replace("(", r"\(").replace(")", r"\)")
        ht += f'RewriteRule "^{src}/?$" "{b}" [R=301,L,NE]\n'
    ht += """
ErrorDocument 404 /404.html

# Compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json image/svg+xml
</IfModule>

# Caching
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png  "access plus 1 year"
  ExpiresByType text/css   "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType text/html  "access plus 1 hour"
</IfModule>

# Correct MIME type for webp
<IfModule mod_mime.c>
  AddType image/webp .webp
</IfModule>

# Security headers
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
"""
    write(".htaccess", ht)
    write(".nojekyll", "")



if __name__ == "__main__":
    build_home()
    build_services_index()
    build_service_pages()
    build_packages()
    build_doctors()
    build_about()
    build_branches_index()
    build_branch_pages()
    build_contact()
    build_404()
    build_support()
    print("built")
