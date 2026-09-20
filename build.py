#!/usr/bin/env python3
"""Builds the Doctors Scans static site into ./out — Stitch-derived design."""
import os, html
from data import *

OUT = "out"

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def wa_link(num, msg):
    from urllib.parse import quote
    return f"https://wa.me/{num}?text={quote(msg)}"

# ---------------------------------------------------------------- icon set
ICONS = {
"call": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.2 1L6.6 10.8z"/></svg>',
"chat": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.24-8.23a8.2 8.2 0 0 1 8.23 8.24c0 4.54-3.69 8.23-8.22 8.23zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.13-.15.17-.25.25-.41.09-.17.04-.31-.02-.43-.06-.13-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.16 0-.43.06-.65.31-.23.25-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.21 3.72.59.25 1.05.4 1.4.52.59.19 1.13.16 1.55.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.29z"/></svg>',
"pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
"clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>',
"check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>',
"check-circle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.5 2.5L16 9"/></svg>',
"arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
"waves": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 8c2 0 2 3 4 3s2-3 4-3 2 3 4 3 2-3 4-3 2 3 4 3"/><path d="M2 14c2 0 2 3 4 3s2-3 4-3 2 3 4 3 2-3 4-3 2 3 4 3"/></svg>',
"biotech": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v5l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/><path d="M7.5 15h9"/></svg>',
"radiology": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><path d="M12 3v4.5M12 16.5V21M3 12h4.5M16.5 12H21"/></svg>',
"ultrasound": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="14" height="10" rx="1.5"/><path d="M7 18h6M10 14v4"/><path d="M14 7l3 0M15.5 5.5v3"/></svg>',
"ct": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="10" r="7"/><circle cx="12" cy="10" r="3"/><path d="M7 20h10M9 17.5v2.5M15 17.5v2.5"/></svg>',
"fetal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3a6 6 0 1 0 4.24 10.24M13 8a3 3 0 1 1-3 3"/><path d="M14 14c1 1.5 1 3.5 0 5"/></svg>',
"biopsy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 5L5 19M15 3l6 6M3 15l6 6"/></svg>',
"liver": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12c0-4 3-8 9-8 5 0 7 3 7 6 0 5-4 9-9 9-4 0-7-3-7-5 0-1 .5-1.7 1.5-2"/></svg>',
"doppler": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h3l2-7 4 14 2-9 2 5h7"/></svg>',
"flask": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 2h6M10 2v6.5L4.5 18a2 2 0 0 0 1.7 3h11.6a2 2 0 0 0 1.7-3L14 8.5V2"/><path d="M7.5 14h9"/></svg>',
"echo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 8.6a5.2 5.2 0 0 0-8.8-3.8 5.2 5.2 0 0 0-8.8 3.8C3.2 13.6 12 20 12 20s8.8-6.4 8.8-11.4z"/><path d="M6 12h2l1.5-3L11 15l1.5-5L14 12h4"/></svg>',
"lungs": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v7"/><path d="M12 10c-1 0-2 1-2.5 2.5L8 18a2.5 2.5 0 0 1-5 0v-4c0-3 2-5 4-6"/><path d="M12 10c1 0 2 1 2.5 2.5L16 18a2.5 2.5 0 0 0 5 0v-4c0-3-2-5-4-6"/></svg>',
"ecg": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h3l2-7 3 14 2-9 1.5 2h9.5"/></svg>',
"star": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.86L12 17.77l-6.18 3.23L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>',
"schedule": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>',
"verified": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.4 1.8 3-.3 1 2.8 2.6 1.4-.8 2.9.8 2.9-2.6 1.4-1 2.8-3-.3L12 22l-2.4-1.8-3 .3-1-2.8-2.6-1.4.8-2.9-.8-2.9 2.6-1.4 1-2.8 3 .3L12 2z"/><path d="M8.5 12.5l2.3 2.3 4.7-4.8"/></svg>',
}
def icon(name, cls="ic"):
    return f'<span class="{cls}">{ICONS[name]}</span>'

# ---------------------------------------------------------------- head
def head(title, desc, canonical, extra_schema=""):
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
<meta name="theme-color" content="#0284c7">

<link rel="preload" href="/assets/fonts/jakarta-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/vendor/bootstrap.min.css?v=6">
<link rel="stylesheet" href="/assets/css/main.css?v=6">
{extra_schema}
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" title="Google Tag Manager"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager -->
<a class="skip-link" href="#main">Skip to content</a>
"""

# ---------------------------------------------------------------- nav
def nav(active=""):
    items = [("/", "Home", "home"), ("/services/", "Services", "services"),
             ("/packages/", "Packages", "packages"), ("/branches/", "Branches", "branches"),
             ("/about/", "About Us", "about"), ("/blog/", "Blog", "blog"),
             ("/contact/", "Contact", "contact")]
    li = ""
    for href, label, key in items:
        cur = ' aria-current="page"' if key == active else ""
        cls = "nav-link active" if key == active else "nav-link"
        li += f'<a class="{cls}" href="{href}"{cur}>{label}</a>'
    return f"""<div class="ticker">
  <div class="container ticker-row">
    <a class="ticker-help" href="tel:{HELPLINE}">{icon('call','ic-sm')}<span>Helpline:</span> {HELPLINE_DISPLAY}</a>
    <span class="ticker-hours">{icon('schedule','ic-sm')}{HOURS_WEEK} &bull; {HOURS_SUN}</span>
  </div>
</div>
<nav class="navbar navbar-expand-xl sticky-top" aria-label="Main navigation">
  <div class="container">
    <a class="navbar-brand" href="/">
      <img src="/assets/images/logo.webp" alt="" width="46" height="46" decoding="async">
      <span class="navbar-brand-text">
        <strong>Doctors Scans &amp; Labs</strong>
        <small>A unit of {LEGAL}</small>
      </span>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarNav" aria-controls="navbarNav"
            aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <div class="nav-links">{li}</div>
      <div class="nav-actions">
        <a class="btn btn-chip" href="/branches/">{icon('pin')}Find Centre</a>
        <a class="btn btn-chip" href="tel:{HELPLINE}">{icon('call')}Call Now</a>
        <button type="button" class="btn btn-whatsapp" data-book="an appointment">
          {icon('chat')}Book on WhatsApp</button>
      </div>
    </div>
  </div>
</nav>
"""

# ---------------------------------------------------------------- footer
def footer():
    links = "".join(f'<li><a href="/branches/{b["slug"]}/">{b["name"]}</a></li>' for b in BRANCHES)
    quick = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in
                    [("/services/", "Services"), ("/packages/", "Health Packages"),
                     ("/about/#team", "Our Doctors"), ("/branches/", "All Branches"),
                     ("/about/", "About Us"), ("/contact/", "Contact")])
    main = BRANCHES[0]
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="row g-4">
      <div class="col-lg-4">
        <div class="footer-brand">
          <img src="/assets/images/logo.webp" alt="" width="46" height="46" loading="lazy" decoding="async">
          <div><strong>Doctors Scans &amp; Labs</strong><span>A unit of {LEGAL}</span></div>
        </div>
        <p class="footer-note">Advanced diagnostic imaging and laboratory services across
        Kollam, Thiruvananthapuram and Thrissur districts.</p>
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
          <a href="tel:{HELPLINE}">{HELPLINE_DISPLAY}</a>
        </p>
        <button type="button" class="btn btn-whatsapp btn-sm" data-book="an appointment">
          {icon('chat')}Book on WhatsApp</button>
        <p class="footer-social">
          <a href="{FACEBOOK}" rel="noopener" aria-label="Doctors Scans on Facebook">
            <svg viewBox="0 0 24 24" aria-hidden="true" width="22" height="22"><path fill="currentColor" d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5.02 3.66 9.18 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.51 1.49-3.9 3.77-3.9 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.88h2.78l-.44 2.91h-2.34V22c4.78-.76 8.44-4.92 8.44-9.94z"/></svg>
          </a>
          <a href="{INSTAGRAM}" rel="noopener" aria-label="Doctors Scans on Instagram">
            <svg viewBox="0 0 24 24" aria-hidden="true" width="22" height="22"><path fill="currentColor" d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16zm0 6.32a3.52 3.52 0 1 0 0 7.04 3.52 3.52 0 0 0 0-7.04zm0 5.81a2.29 2.29 0 1 1 0-4.58 2.29 2.29 0 0 1 0 4.58zm4.48-5.95a.82.82 0 1 1-1.64 0 .82.82 0 0 1 1.64 0z"/></svg>
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
          {"".join(f'''<a class="picker-item" href="#" data-wa="{b['wa']}" data-tel="{b['phone']}" data-slug="{b['slug']}">
            <span class="picker-name">{b['name']}</span>
            <span class="picker-sub">{b['landmark']}</span>
            <span class="picker-num">{b['display']}</span>
          </a>''' for b in BRANCHES)}
        </div>
      </div>
    </div>
  </div>
</div>

<a class="wa-float" href="#" data-book="an appointment" aria-label="Book on WhatsApp">{icon('chat')}</a>

<script src="/assets/vendor/bootstrap.bundle.min.js?v=6" defer></script>
<script src="/assets/js/main.js?v=6" defer></script>
</body>
</html>
"""

def wa_btn(service, cls="btn btn-whatsapp", at=None, label=None):
    scope = f' data-at="{",".join(at)}"' if at else ""
    label = label or "Book on WhatsApp"
    return f'<button type="button" class="{cls}" data-book="{html.escape(service)}"{scope}>{icon("chat")}{label}</button>'

def call_btn(cls="btn btn-outline-brand", at=None, label="Call"):
    scope = f' data-at="{",".join(at)}"' if at else ""
    return f'<button type="button" class="{cls}" data-call="1"{scope}>{icon("call")}{label}</button>'

def crumbs(trail):
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

def hero(cls, h1, sub, extra=""):
    return f"""<header class="page-hero {cls}">
  <span class="hero-sweep" aria-hidden="true"></span>
  <div class="container">
    <h1>{h1}</h1>
    <span class="hero-rule" aria-hidden="true"></span>
    <p class="hero-sub">{sub}</p>
    {extra}
  </div>
</header>
"""

# ================================================================ SCHEMA
def branch_schema(b, service_list=False):
    svc = ""
    if service_list:
        svc = ',"availableService":[' + ",".join(
            f'{{"@type":"MedicalTest","name":"{s["name"]}"}}' for s in services_for(b)) + "]"
    return f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"DiagnosticLab",
"@id":"{SITE}/branches/{b['slug']}/#business",
"name":"Doctors Scans & Labs, {b['name']}",
"parentOrganization":{{"@type":"Organization","name":"{LEGAL}","url":"{SITE}/"}},
"url":"{SITE}/branches/{b['slug']}/",
"image":"{SITE}/assets/images/og-image.jpg",
"logo":"{SITE}/assets/images/logo.jpg",
"telephone":"{b['phone']}",
"address":{{"@type":"PostalAddress","streetAddress":"{b['address']}",
"addressLocality":"{b['locality']}","addressRegion":"{b['region']}",
"postalCode":"{b['postal']}","addressCountry":"IN"}},
"geo":{{"@type":"GeoCoordinates","latitude":{b['lat']},"longitude":{b['lng']}}},
"hasMap":"{b['map']}",
"openingHoursSpecification":[
{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"07:00","closes":"19:30"}},
{{"@type":"OpeningHoursSpecification","dayOfWeek":"Sunday","opens":"07:00","closes":"14:00"}}],
"sameAs":["{INSTAGRAM}","{FACEBOOK}"]{svc}}}
</script>"""

ORG_SCHEMA = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"MedicalOrganization",
"@id":"{SITE}/#organization","name":"{BRAND}","legalName":"{LEGAL}",
"url":"{SITE}/","logo":"{SITE}/assets/images/logo.jpg",
"image":"{SITE}/assets/images/og-image.jpg",
"telephone":"{HELPLINE}","sameAs":["{INSTAGRAM}","{FACEBOOK}"],
"department":[{",".join(f'{{"@id":"{SITE}/branches/{b["slug"]}/#business"}}' for b in BRANCHES)}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebSite","url":"{SITE}/","name":"{BRAND}"}}
</script>"""

# ================================================================ SHARED CARD BUILDERS
def service_card(s, compact=False):
    badge = ""
    if len(s["at"]) < len(BRANCHES):
        only = branches_for(s)[0]["name"]
        badge = f'<span class="svc-badge">Available at {only}</span>'
    return f"""<div class="svc-card{' svc-card-badged' if badge else ''}">
  <div class="svc-card-top">
    <div class="svc-icon">{icon(s['icon'], "ic-fill")}</div>
    {badge}
  </div>
  <h3><a href="/services/{s['slug']}/">{s['name']}</a></h3>
  <p>{s['short']}</p>
  <div class="svc-card-foot">
    <span class="svc-tag">{s['tag']}</span>
    {wa_btn(s['name'], cls="svc-book", at=s['at'], label="Book on WhatsApp")}
  </div>
</div>"""

def package_card(p):
    ribbon = f'<div class="pkg-ribbon">{p["badge"]}</div>' if p["badge"] and len(p["badge"]) < 24 else ""
    cat_pill = f'<span class="pkg-cat">{p["badge"]}</span>' if p["badge"] and not ribbon else f'<span class="pkg-cat">{p["category"]}</span>'
    save_pill = f'<span class="pkg-save">Save {p["save"]}</span>' if p["save"] else ""
    tests = "".join(f'<li>{icon("check-circle")}<span>{t}</span></li>' for t in p["tests"])
    wa_msg = f'{p["name"]} package'
    return f"""<div class="pkg-card">
  {ribbon}
  <div class="pkg-card-head">
    <span class="pkg-cat">{p['category']}</span>
    {save_pill}
  </div>
  <h3>{p['name']}</h3>
  <p>{p['short']}</p>
  <div class="pkg-price"><span class="pkg-now">{p['price']}</span><span class="pkg-orig">{p['orig']}</span></div>
  <div class="pkg-tests">
    <p class="pkg-tests-label">{p['testlabel']}</p>
    <ul>{tests}</ul>
  </div>
  {wa_btn(wa_msg, cls="btn btn-whatsapp w-100 mt-3")}
</div>"""

def _nowrap_tail(name):
    """Join the last two words of a name with a non-breaking space, so a
    trailing initial (e.g. the 'G' in 'Sabarinadh M G') never wraps onto its
    own line by itself."""
    parts = name.split(" ")
    if len(parts) < 2:
        return name
    return " ".join(parts[:-2] + [parts[-2] + "\u00a0" + parts[-1]])

def doctor_card(d):
    slug = d["name"].lower().replace("dr.","").strip().replace(" ","-").replace(".","")
    return f"""<div class="doc-card">
  <div class="doc-photo"><img src="/assets/images/doctors/{slug}.webp" alt="{d['name']}"
       width="200" height="200" loading="lazy" decoding="async"></div>
  <span class="doc-role">{d['role']}</span>
  <h3>{_nowrap_tail(d['name'])}</h3>
  <p class="doc-qual">{d['qual']}</p>
  <span class="doc-sub">{d['sub']}</span>
</div>"""

def branch_card(b, full=True):
    badge = f'<div class="branch-badge">{b["badge"]}</div>' if b.get("badge") else ""
    landline = (f'<div class="branch-row">{icon("call")}'
                f'<a href="tel:{b["landline"]}">{b["landline_display"]}</a></div>'
                if b.get("landline") else "")
    return f"""<div class="branch-card{' branch-card-flag' if badge else ''}">
  {badge}
  <div class="branch-card-head">{icon('pin')}<h3>{b['name']}</h3></div>
  <p class="branch-addr">{b['landmark']}</p>
  <p class="branch-svc">{b['services_line']}</p>
  <div class="branch-rows">
    <div class="branch-row">
      {icon('call')}
      <a href="tel:{b['phone']}">{b['display']}</a>
      <a class="branch-call-chip" href="tel:{b['phone']}">{icon('call')}Call</a>
    </div>
    {landline}
    <div class="branch-row branch-row-muted">
      {icon('schedule')}<span>{HOURS_WEEK} &bull; {HOURS_SUN}</span>
    </div>
  </div>
  <div class="branch-actions">
    <a class="btn btn-whatsapp w-100" rel="noopener"
       href="{wa_link(b['wa'], f"Hello Doctors Scans {b['name']}, I would like to book an appointment.")}">
      {icon('chat')}Book on WhatsApp</a>
    <a class="btn btn-outline-brand w-100" href="/branches/{b['slug']}/">Centre Details</a>
  </div>
</div>"""

# ================================================================ HOME
def build_home():
    branch_strip = "".join(f'<span class="hero-chip-branch">{b["name"]}</span>' for b in BRANCHES)
    # Homepage shows highlights only — full lists live on their dedicated pages.
    svc_cards = "".join(service_card(s) for s in SERVICES[:6])
    pkg_cards = "".join(package_card(p) for p in
                        [p for p in PACKAGES if p["badge"]][:3])
    doc_cards = "".join(doctor_card(d) for d in DOCTORS[:6])
    branch_cards = "".join(branch_card(b) for b in BRANCHES)

    title = "Doctors Scans &amp; Labs | Diagnostic Centres Across Kerala"
    desc = (f"Ultrasound, CT scan, fetal imaging, Doppler, echo, FibroScan and laboratory "
            f"services across {len(BRANCHES)} centres in Kerala. Open 7 AM daily.")
    h = head(title, desc, "/", ORG_SCHEMA)
    body = f"""{nav('home')}
<main id="main">
<header class="home-hero">
  <span class="home-hero-glow g1" aria-hidden="true"></span>
  <span class="home-hero-glow g2" aria-hidden="true"></span>
  <div class="container">
    <div class="home-hero-topline">
      <span class="pill pill-live">
        <span class="pulse-dot"></span>
        {LEGAL}<em> &bull; Centres Across Kerala</em>
      </span>
    </div>
    <div class="home-hero-grid">
      <div class="home-hero-copy">
        <h1>Advanced Diagnostic <span class="grad">Imaging &amp; Laboratory</span> Services</h1>
        <p class="home-hero-lede">A unit of {LEGAL}. Providing cutting-edge Radiology,
        Advanced Fetal Imaging, and Fully Automated Laboratory Services across Kerala.</p>
        <div class="hero-highlights">
          <span class="pill">{icon('waves')}Ultrasound &amp; Doppler Scans</span>
          <span class="pill">{icon('verified')}CT Scan (Parippally)</span>
          <span class="pill">{icon('biotech')}Automated Multi-Branch Labs</span>
        </div>
        <div class="hero-cta">
          {wa_btn("a scan or lab test", cls="btn btn-whatsapp btn-lg")}
          <a class="btn btn-grad btn-lg" href="/branches/">{icon('pin')}Find Nearest Branch</a>
        </div>
      </div>
      <div class="home-hero-visual">
        <div class="hero-photo-frame">
          <img src="/assets/images/banner-home.webp" alt="Clinical ultrasound examination at Doctors Scans" width="640" height="480" decoding="async">
          <span class="hero-photo-badge"><span class="pulse-dot"></span>Open 7 AM Daily &bull; Sunday Services</span>
          <div class="hero-photo-card">
            {icon('radiology')}
            <div>
              <strong>Comprehensive Diagnostic Network</strong>
              <span>{" &bull; ".join(b['name'] for b in BRANCHES)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</header>

<section class="section" id="services">
  <div class="container">
    <div class="section-head-row">
      <div>
        <span class="eyebrow">Comprehensive Diagnostic Services</span>
        <h2 class="section-title-lg">Services We Provide</h2>
        <p class="section-lede-lg">State-of-the-art Radiology Imaging and Laboratory
        Services calibrated for accuracy, early detection, and prompt patient reporting.</p>
      </div>
      <a class="btn btn-whatsapp shrink-0" href="{wa_link(BRANCHES[0]['wa'], 'I want to enquire about services')}" rel="noopener">
        {icon('chat')}Enquire on WhatsApp</a>
    </div>
    <div class="svc-grid">{svc_cards}</div>
    <div class="view-all"><a class="btn btn-outline-brand btn-lg" href="/services/">View All Services</a></div>
  </div>
</section>

<section class="section section-alt" id="packages">
  <div class="container">
    <div class="text-center-head">
      <span class="eyebrow">Preventive Health Screening</span>
      <h2 class="section-title-lg">Health Checkup Packages</h2>
      <p class="section-lede-lg">Tailored screening packages designed to detect health concerns early.</p>
    </div>
    <div class="promo-banner">
      <div class="promo-banner-text">{icon('verified')}
        <p><strong>Promotional rates active across all centres. Stated prices include
        all listed parameters and tests.</strong></p>
      </div>
      <a class="btn btn-whatsapp shrink-0" href="{wa_link(BRANCHES[0]['wa'], 'Please send current package pricing and details')}" rel="noopener">
        {icon('chat')}Get Pricing on WhatsApp</a>
    </div>
    <div class="pkg-grid">{pkg_cards}</div>
    <div class="view-all"><a class="btn btn-outline-brand btn-lg" href="/packages/">View All Packages</a></div>
  </div>
</section>

<section class="section" id="doctors">
  <div class="container">
    <div class="text-center-head">
      <span class="eyebrow">Clinical Leadership</span>
      <h2 class="section-title-lg">Our Team of Doctors</h2>
      <p class="section-lede-lg">Our team consists of Dedicated Radiologists &amp; Experienced
      Doctors actively supporting &amp; working across our diagnostic centres.</p>
    </div>
    <div class="doc-grid">{doc_cards}</div>
    <div class="view-all"><a class="btn btn-outline-brand btn-lg" href="/about/#team">Meet Our Full Team</a></div>
  </div>
</section>

<section class="section section-alt" id="branches">
  <div class="container">
    <div class="text-center-head">
      <span class="eyebrow">Network of Excellence</span>
      <h2 class="section-title-lg">Our Main Branches &amp; Centres</h2>
      <p class="section-lede-lg">Conveniently located near major hospitals across Kollam,
      Thiruvananthapuram, and Thrissur districts.</p>
    </div>
    <div class="branch-grid">{branch_cards}</div>
    <div class="view-all"><a class="btn btn-outline-brand btn-lg" href="/branches/">All Branch Details</a></div>
  </div>
</section>

<section class="cta-strip">
  <div class="container cta-strip-row">
    <div>
      <h2>Committed to Clinical Precision &amp; Compassionate Care</h2>
      <p>Operating across Kerala with Advanced Ultrasound &amp; Doppler Modalities,
      Operational Fetal Imaging, and High-Throughput Automated Laboratories.</p>
    </div>
    <div class="cta-strip-actions">
      {wa_btn("an appointment", cls="btn btn-whatsapp btn-lg", label="Chat on WhatsApp")}
      <a class="btn btn-outline-white btn-lg" href="tel:{HELPLINE}">{icon('call')}Call Now</a>
    </div>
  </div>
</section>
</main>
{footer()}"""
    write("index.html", h + body)

# ================================================================ SERVICES
def build_services_index():
    cards = "".join(service_card(s) for s in SERVICES)
    cb, cbld = crumbs([("/", "Home"), ("/services/", "Services")])
    title = "Diagnostic Services | Doctors Scans &amp; Labs, Kerala"
    desc = (f"Ultrasound, CT scan, advanced fetal imaging, Doppler, echo, FibroScan, PFT, "
            f"ECG and laboratory services across our {len(BRANCHES)} centres in Kerala.")
    write("services/index.html", head(title, desc, "/services/", cbld) +
          nav('services') + '<main id="main">' +
          hero('hero-services', 'Our services',
               f'{len(SERVICES)} diagnostic services, available across our centres.') + cb + f"""
<section class="section"><div class="container"><div class="svc-grid">{cards}</div></div></section>
</main>""" + footer())

def build_service_pages():
    for s in SERVICES:
        at = branches_for(s)
        avail = "".join(f'<a class="rel-chip" href="/branches/{b["slug"]}/">{b["name"]}</a>' for b in at)
        others = "".join(f'<a class="rel-chip" href="/services/{o["slug"]}/">{o["name"]}</a>'
                         for o in SERVICES if o["slug"] != s["slug"])
        cb, cbld = crumbs([("/", "Home"), ("/services/", "Services"), (f"/services/{s['slug']}/", s["name"])])
        schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"MedicalTest","name":"{s['name']}",
"description":"{html.escape(s['desc'])}","url":"{SITE}/services/{s['slug']}/",
"provider":{{"@id":"{SITE}/#organization"}}}}
</script>""" + cbld
        title = f"{s['name']} | Doctors Scans &amp; Labs, Kerala"
        note = (f"Opens WhatsApp for our {at[0]['name']} centre with your message ready to send."
                if len(at) == 1 else
                "Choose your nearest centre and we will open WhatsApp with your message ready to send.")
        write(f"services/{s['slug']}/index.html",
              head(title, s["desc"], f"/services/{s['slug']}/", schema) +
              nav('services') + '<main id="main">' +
              hero('hero-services', s["name"], s["short"]) + cb + f"""
<section class="section">
  <div class="container">
    <div class="row g-5 align-items-start">
      <div class="col-lg-6">
        <div class="svc-detail-icon">{icon(s['icon'], "ic-fill")}</div>
        <span class="svc-tag lg">{s['tag']}</span>
      </div>
      <div class="col-lg-6">
        <h2>About this test</h2>
        <p class="lede">{s['long']}</p>
        <div class="svc-book">
          {wa_btn(s['name'], cls="btn btn-whatsapp btn-lg w-100", at=s['at'])}
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
    <h2 class="section-title-lg text-center">Other services</h2>
    <div class="chip-row justify-content-center">{others}</div>
  </div>
</section>
</main>""" + footer())

# ================================================================ PACKAGES
def build_packages():
    cards = "".join(package_card(p) for p in PACKAGES)
    cb, cbld = crumbs([("/", "Home"), ("/packages/", "Health Packages")])
    title = "Health Checkup Packages &amp; Prices | Doctors Scans &amp; Labs"
    desc = ("Discounted health checkup packages with published prices — master, thyroid, "
            "PCOS, diabetic and full body checkups. Book on WhatsApp.")
    write("packages/index.html", head(title, desc, "/packages/", cbld) +
          nav('packages') + '<main id="main">' +
          hero('hero-packages', 'Health checkup packages',
               'Tailored screening packages designed to detect health concerns early.') + cb + f"""
<section class="section"><div class="container">
  <div class="promo-banner">
    <div class="promo-banner-text">{icon('verified')}
      <p><strong>Promotional rates active across all centres. Stated prices include
      all listed parameters and tests.</strong></p>
    </div>
    <a class="btn btn-whatsapp shrink-0" href="{wa_link(BRANCHES[0]['wa'], 'Please send current package pricing and details')}" rel="noopener">
      {icon('chat')}Get Pricing on WhatsApp</a>
  </div>
  <div class="pkg-grid">{cards}</div>
</div></section>
</main>""" + footer())

# ================================================================ ABOUT
def build_about():
    cb, cbld = crumbs([("/", "Home"), ("/about/", "About Us")])
    title = "About Us | Doctors Scans &amp; Labs"
    desc = (f"Doctors Scans & Labs is a diagnostic imaging and laboratory network with "
            f"{len(BRANCHES)} centres across Kollam, Thiruvananthapuram and Thrissur districts in Kerala.")
    doc_cards = "".join(doctor_card(d) for d in DOCTORS)
    doc_ld = ",".join(f'{{"@type":"Physician","name":"{d["name"]}","medicalSpecialty":"{d["role"]}"}}'
                      for d in DOCTORS)
    schema = (f'<script type="application/ld+json">{{"@context":"https://schema.org",'
              f'"@type":"ItemList","itemListElement":[{doc_ld}]}}</script>' + cbld)
    write("about/index.html", head(title, desc, "/about/", schema) +
          nav('about') + '<main id="main">' +
          hero('hero-about', 'About us', 'Your health, our lifelong commitment.') + cb + f"""
<section class="section">
  <div class="container narrow">
    <h2>About Us</h2>
    <p class="lede">We are a team of doctors who came together with a shared vision to
    uplift healthcare in the rural and semi-urban communities of Kerala. What began as a
    single diagnostic centre has grown into a network across multiple districts, bringing
    advanced imaging, laboratory services and specialist expertise closer to the people
    who need them.</p>

    <p>Our centres are located close to government hospitals, helping patients access
    reliable and affordable diagnostics without the need to travel long distances. With
    modern technology, consultant radiologists, skilled healthcare professionals and a
    strong focus on accurate and timely reporting, we are committed to making every
    diagnostic experience more accessible, reassuring and patient-focused.</p>

    <p>When you need a scan or diagnostic test, you need more than a report &mdash; you
    need confidence, clarity and care.</p>

    <p>Our vision is simple: bring the standards of advanced diagnostics closer to
    everyone, because quality healthcare should be accessible to all, wherever they
    live.</p>
  </div>
</section>

<section class="section section-alt" id="team">
  <div class="container">
    <div class="text-center-head">
      <span class="eyebrow">Clinical Leadership</span>
      <h2 class="section-title-lg">Our Team</h2>
      <p class="section-lede-lg">Our team consists of Dedicated Radiologists &amp; Experienced
      Doctors actively supporting &amp; working across our diagnostic centres.</p>
    </div>
    <div class="doc-grid">{doc_cards}</div>
  </div>
</section>

<section class="section">
  <div class="container narrow">
    <div class="cta-band">
      <h2>Book at your nearest centre</h2>
      <p>Pick a centre and message us on WhatsApp.</p>
      {wa_btn("an appointment", cls="btn btn-whatsapp btn-lg")}
    </div>
  </div>
</section>
</main>""" + footer())

# ================================================================ BRANCHES
def build_branches_index():
    cards = "".join(branch_card(b) for b in BRANCHES)
    cb, cbld = crumbs([("/", "Home"), ("/branches/", "Branches")])
    title = "Our Branches | Doctors Scans &amp; Labs"
    desc = (f"{len(BRANCHES)} Doctors Scans & Labs centres across Kollam, Thiruvananthapuram "
            f"and Thrissur. Addresses, phone numbers and directions.")
    write("branches/index.html", head(title, desc, "/branches/", cbld) +
          nav('branches') + '<main id="main">' +
          hero('hero-contact', 'Our branches',
               f'{len(BRANCHES)} centres across Kollam, Thiruvananthapuram and Thrissur districts.') + cb + f"""
<section class="section"><div class="container"><div class="branch-grid">{cards}</div></div></section>
</main>""" + footer())

def build_branch_pages():
    for b in BRANCHES:
        cb, cbld = crumbs([("/", "Home"), ("/branches/", "Branches"), (f"/branches/{b['slug']}/", b["name"])])
        schema = branch_schema(b, service_list=True) + cbld
        title = f"Scan Centre in {b['name']} | Doctors Scans &amp; Labs"
        desc = (f"Scan centre and diagnostic lab at {b['landmark']}. Ultrasound, Doppler, "
                f"echo and lab tests. Call {b['display']}.")
        svc = "".join(f'<a class="rel-chip" href="/services/{s["slug"]}/">{s["name"]}</a>' for s in services_for(b))
        others = "".join(f'<a class="rel-chip" href="/branches/{o["slug"]}/">{o["name"]}</a>'
                         for o in BRANCHES if o["slug"] != b["slug"])
        landline = (f'<p class="ct-row"><span>Landline</span>'
                    f'<a href="tel:{b["landline"]}">{b["landline_display"]}</a></p>'
                    if b["landline"] else "")
        write(f"branches/{b['slug']}/index.html",
              head(title, desc, f"/branches/{b['slug']}/", schema) +
              nav('branches') + '<main id="main">' +
              hero('hero-contact', f"Doctors Scans &amp; Labs, {b['name']}", b["landmark"]) + cb + f"""
<section class="section">
  <div class="container">
    <div class="row g-5">
      <div class="col-lg-5">
        <h2>Contact this centre</h2>
        <p class="lede">{b['blurb']}</p>
        <div class="contact-block">
          <p class="ct-row"><span>Address</span>{b['address']}, {b['locality']}, {b['region']} {b['postal']}</p>
          <p class="ct-row"><span>Phone</span><a href="tel:{b['phone']}">{b['display']}</a></p>
          {landline}
          <p class="ct-row"><span>Hours</span>{HOURS_WEEK}<br>{HOURS_SUN}</p>
        </div>
        <div class="d-grid gap-2 mt-4">
          <a class="btn btn-whatsapp btn-lg" rel="noopener"
             href="{wa_link(b['wa'], f"Hello Doctors Scans {b['name']}, I would like to book an appointment.")}">
            {icon('chat')}Message {b['name']} on WhatsApp</a>
          <a class="btn btn-outline-brand btn-lg" href="tel:{b['phone']}">{icon('call')}Call {b['display']}</a>
          <a class="btn btn-link" href="{b['map']}" rel="noopener">Open in Google Maps</a>
        </div>
      </div>
      <div class="col-lg-7">
        <div class="branch-map">
          <iframe src="{b['embed']}" title="Map showing Doctors Scans &amp; Labs, {b['name']}"
                  loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2 class="section-title-lg">Services at this centre</h2>
    <div class="chip-row">{svc}</div>
    <h2 class="section-title-lg mt-5">Our other centres</h2>
    <div class="chip-row">{others}</div>
  </div>
</section>
</main>""" + footer())

# ================================================================ CONTACT
def build_contact():
    b = BRANCHES[0]
    cards = "".join(branch_card(x) for x in BRANCHES)
    cb, cbld = crumbs([("/", "Home"), ("/contact/", "Contact")])
    title = "Contact Us | Doctors Scans &amp; Labs, Kerala"
    desc = (f"Call or WhatsApp any of our {len(BRANCHES)} centres across Kerala. "
            f"Open {HOURS_WEEK.lower()}, {HOURS_SUN.lower()}.")
    write("contact/index.html", head(title, desc, "/contact/", branch_schema(b) + cbld) +
          nav('contact') + '<main id="main">' +
          hero('hero-contact', 'Contact us', 'Message the centre nearest you and we will take it from there.') + cb + f"""
<section class="section">
  <div class="container">
    <div class="row g-4 info-row">
      <div class="col-md-4"><div class="info-box">
        <h2 class="h6">Opening hours</h2><p>{HOURS_WEEK}<br>{HOURS_SUN}</p></div></div>
      <div class="col-md-4"><div class="info-box">
        <h2 class="h6">Helpline</h2><p><a href="tel:{HELPLINE}">{HELPLINE_DISPLAY}</a></p></div></div>
      <div class="col-md-4"><div class="info-box">
        <h2 class="h6">Book a scan</h2><p>Pick your centre below and message us on WhatsApp.</p></div></div>
    </div>
    <h2 class="section-title-lg mt-5">All {len(BRANCHES)} centres</h2>
    <div class="branch-grid">{cards}</div>
  </div>
</section>
</main>""" + footer())

# ================================================================ BLOG
def build_blog_index():
    cb, cbld = crumbs([("/", "Home"), ("/blog/", "Blog")])
    title = "Blog | Doctors Scans &amp; Labs"
    desc = ("Articles on diagnostic imaging, health screening and preventive care from "
            "Doctors Scans & Labs.")
    if BLOG_POSTS:
        cards = "".join(f"""<article class="blog-card">
      <a href="/blog/{p['slug']}/" class="blog-card-link">
        <span class="pkg-cat">{p['category']}</span>
        <h2>{p['title']}</h2>
        <p>{p['excerpt']}</p>
        <span class="blog-meta">{p['author']} &bull; {p['date']}</span>
      </a>
    </article>""" for p in sorted(BLOG_POSTS, key=lambda x: x['date'], reverse=True))
        body = f'<div class="blog-grid">{cards}</div>'
    else:
        body = f"""<div class="blog-empty">
      <div class="svc-detail-icon" style="margin:0 auto 1.25rem;">{icon('flask', "ic-fill")}</div>
      <h2>New articles coming soon</h2>
      <p class="lede">We're putting together practical guides on diagnostic imaging,
      health screening and preventive care. Check back soon, or message us directly
      if you have a question you'd like answered.</p>
      {wa_btn("a question", cls="btn btn-whatsapp btn-lg", label="Ask us on WhatsApp")}
    </div>"""
    write("blog/index.html", head(title, desc, "/blog/", cbld) +
          nav('blog') + '<main id="main">' +
          hero('hero-about', 'Blog', 'Guides and updates from Doctors Scans &amp; Labs.') + cb + f"""
<section class="section"><div class="container">{body}</div></section>
</main>""" + footer())

def build_blog_posts():
    for p in BLOG_POSTS:
        cb, cbld = crumbs([("/", "Home"), ("/blog/", "Blog"), (f"/blog/{p['slug']}/", p["title"])])
        schema = f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(p['title'])}",
"datePublished":"{p['date']}","author":{{"@type":"Person","name":"{p['author']}"}},
"publisher":{{"@id":"{SITE}/#organization"}}}}
</script>""" + cbld
        body_html = "".join(f"<p>{para}</p>" for para in p["body"])
        write(f"blog/{p['slug']}/index.html",
              head(f"{p['title']} | Doctors Scans &amp; Labs Blog", p["excerpt"],
                   f"/blog/{p['slug']}/", schema) +
              nav('blog') + '<main id="main">' +
              hero('hero-about', p['title'], f"{p['author']} &bull; {p['date']}") + cb + f"""
<section class="section"><div class="container narrow">{body_html}</div></section>
</main>""" + footer())

def build_404():
    OLD_URLS = {
        "/services/ultrasonography (usg)":         "/services/ultrasonography-usg/",
        "/services/advanced fetal medicine":       "/services/advanced-fetal-medicine/",
        "/services/usg guided procedures":         "/services/usg-guided-procedures/",
        "/services/fibroscan & elastography":      "/services/fibroscan-elastography/",
        "/services/doppler studies":               "/services/doppler-studies/",
        "/services/echocardiography (echo)":       "/services/echocardiography/",
        "/services/laboratory services":           "/services/laboratory-services/",
        "/services/pulmonary function test (pft)": "/services/pulmonary-function-test/",
        "/services/colonoscopy & endoscopy":       "/services/",
        "/services/fetal interventions":           "/services/",
        "/services/adult-echocardiography":        "/services/echocardiography/",
        "/header.html": "/", "/footer.html": "/",
    }
    import json as _json
    table = _json.dumps(OLD_URLS, indent=2)
    redirect_js = rf"""<script>
(function () {{
  var MOVED = {table};
  var p = decodeURIComponent(location.pathname).toLowerCase().replace(/\/+$/, "");
  if (MOVED[p]) {{ location.replace(MOVED[p]); return; }}
  if (p.indexOf("/services") === 0) {{ location.replace("/services/"); return; }}
  var simple = {{"/packages": "/packages/", "/doctors": "/about/#team",
                "/about": "/about/", "/contact": "/contact/"}};
  if (simple[p]) {{ location.replace(simple[p]); }}
}})();
</script>"""
    write("404.html", head("Page not found | Doctors Scans &amp; Labs",
                          "The page you were looking for could not be found.", "/404.html", redirect_js) +
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
    urls = ["/", "/services/", "/packages/", "/branches/", "/blog/", "/about/", "/contact/"]
    urls += [f"/services/{s['slug']}/" for s in SERVICES]
    urls += [f"/branches/{b['slug']}/" for b in BRANCHES]
    urls += [f"/blog/{p['slug']}/" for p in BLOG_POSTS]
    pri = {"/": "1.0", "/services/": "0.9", "/branches/": "0.9", "/packages/": "0.9", "/contact/": "0.8"}
    entries = "".join(
        f"  <url><loc>{SITE}{u}</loc><changefreq>monthly</changefreq>"
        f"<priority>{pri.get(u, '0.7')}</priority></url>\n" for u in urls)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f'{entries}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

    R = [("/Services/", "/services/"), ("/Packages/", "/packages/"),
         ("/Doctors/", "/about/"), ("/About/", "/about/"), ("/Contact/", "/contact/")]
    write("_redirects", "".join(f"{a}  {b}  301\n" for a, b in R) +
          "/header.html  /  301\n/footer.html  /  301\n")

    ht = """# ---- Doctors Scans .htaccess (Apache / cPanel hosting) ----
Options -Indexes
DirectoryIndex index.html

RewriteEngine On
RewriteCond %{HTTPS} !=on
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]
RewriteCond %{HTTP_HOST} ^doctorsscans\\.com [NC]
RewriteRule ^(.*)$ https://www.doctorsscans.com/$1 [R=301,L]

ErrorDocument 404 /404.html

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json image/svg+xml
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png  "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType text/css   "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType text/html  "access plus 1 hour"
</IfModule>
<IfModule mod_mime.c>
  AddType image/webp .webp
  AddType font/woff2 .woff2
</IfModule>
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
    build_about()
    build_branches_index()
    build_branch_pages()
    build_blog_index()
    build_blog_posts()
    build_contact()
    build_404()
    build_support()
    print("built")
