# Doctors Scans & Labs — website

Rebuilt from the original files, with the problems from the audit fixed.
Plain static HTML. No build step, no database, no npm. Edit a file, upload it, done.

---

## What's in here

```
/
├── index.html                    Home
├── services/index.html           Services list
│   └── <11 service pages>/       includes ct-scan (Parippally only)
├── packages/index.html           Health packages
├── doctors/index.html            Doctors
├── branches/index.html           All six centres
│   └── parippally/ kadakkal/ chirayinkeezhu/
│       kottarakkara/ karunagappalli/ kottiyam/
├── about/index.html
├── contact/index.html
├── 404.html                      Also forwards old URLs to new ones
├── robots.txt      sitemap.xml   site.webmanifest
├── .htaccess       Apache/cPanel config + old-URL redirects
├── _redirects      Same redirects, for Cloudflare Pages or Netlify
├── .nojekyll       Only needed if you use GitHub Pages
└── assets/
    ├── css/main.css              All site styling
    ├── js/main.js                Branch picker only
    ├── vendor/                   Bootstrap (self-hosted, trimmed)
    └── images/                   All images, WebP
```

**25 pages, 70 files, 1.5 MB total.** Old URLs from the previous site are caught
by `404.html`, which forwards them to the right new page. Every page's content is in its own HTML file —
nothing is loaded in by JavaScript any more.

---

## How the WhatsApp booking works

Every "Book on WhatsApp" button opens a small panel listing all six centres.
The patient taps their centre, and WhatsApp opens **for that centre's number**
with the message already written, including the service they were looking at.

Example: someone on the Doppler Studies page taps Book, chooses Kottarakkara,
and WhatsApp opens to 85899 36524 saying
*"Hello Doctors Scans, I would like to book Doppler Studies."*

On the individual branch pages, the WhatsApp button is a **direct link** to that
branch — no picker, because you're already on that centre's page.

The floating green button in the bottom-right corner does the same thing from
anywhere on the site.

### If JavaScript is blocked
The picker needs JavaScript. If it fails to load, the buttons send people to
`/branches/` instead, where every centre has a plain WhatsApp link and a phone
number. Nothing is unreachable.

---

## Changing things

### Phone or WhatsApp number for a centre
Search for the old number across all files and replace it. The number appears in
three forms, so replace all three:

| Form | Example | Where |
|---|---|---|
| Link format | `tel:+919995236524` | phone links |
| Display format | `99952 36524` | visible text |
| WhatsApp format | `919995236524` | `data-wa` and `wa.me` links |

On Windows use Notepad++ (Search → Find in Files). On Mac use BBEdit or VS Code.

### Text on a page
Open that page's `index.html` and edit the text between the tags. Don't touch
anything inside `<script type="application/ld+json">` unless you also update the
visible text to match — that block is what Google reads.

### Doctor photos
Replace `/assets/images/doctor-placeholder.webp`. To give each doctor their own
photo, save them as `dr-sabarinath.webp`, `dr-jithin.webp` etc. and update the
`src` on the doctor cards in `doctors/index.html` and `index.html`.

Crop square, around 500×500. Every doctor currently shares one placeholder.

### Adding a package price
In `packages/index.html`, inside a package card, add a line after the description:

```html
<p class="fw-bold">₹1,850</p>
```

### The menu, footer, or anything that appears on every page
This is the one trade-off in this build. The header and footer are written into
all 24 files, so a change to either means a find-and-replace across all of them.

That was a deliberate choice: it's why Google can now read your pages. Adding a
menu item is a five-minute job a few times a year. Use Find in Files, replace the
whole `<ul class="navbar-nav ...">` block, and check one page afterwards.

---

## Deploying

### Option A — your current cPanel host
1. Log in to cPanel → File Manager → `public_html`
2. **Back up what's there first.** Select all, Compress, download the zip.
3. Delete the old files and upload the contents of this folder.
4. Make sure `.htaccess` uploads — File Manager hides dotfiles until you turn on
   Settings → Show Hidden Files.
5. Visit the site and check one old URL redirects, e.g.
   `doctorsscans.com/Services/Doppler%20Studies/` should land on
   `/services/doppler-studies/`.

### Option B — Cloudflare Pages (free, faster in India)
1. Push this folder to a GitHub repository.
2. Cloudflare dashboard → Workers & Pages → Create → Connect to Git.
3. Build command: leave blank. Output directory: `/`.
4. Add `doctorsscans.com` as a custom domain.

`_redirects` handles the old URLs. `.htaccess` is ignored there — harmless.

### Option C — GitHub Pages
Works, but has no redirect support, so the old URLs will 404. Only use this if
you're willing to lose the existing rankings on those pages.

---

## After you go live

1. **Google Search Console** → submit `https://www.doctorsscans.com/sitemap.xml`
2. **Check indexing** on one branch page after a week
3. **Google Business Profile** — for each of the six branches, set the website
   field to that branch's page, not the homepage:
   - Parippally → `/branches/parippally/`
   - Kadakkal → `/branches/kadakkal/`
   - …and so on

   This is the single highest-value thing you can do after launch. It connects
   each Business Profile to a page with matching address and phone data, which is
   what drives the map results.
4. **Check GTM is firing** — Tag Assistant, or just watch realtime in Analytics.
   The container ID `GTM-53ZJDDC3` is now in the `<head>` of every page rather
   than injected late, so numbers should go up a little.

---

## Things I could not decide for you

These are marked so you don't forget them.

| Item | What's needed |
|---|---|
| **CT scan image** | `/assets/images/ct-scan.webp` is a placeholder graphic I drew. Replace it with a photo of your actual scanner — a real photo performs much better. |
| **MRI / X-ray / mammography** | Removed from About. CT is now included (Parippally). Add the others back only if you actually have them. |
| **Karunagappalli number** | Was written `08943652466`. I've used `+91 89436 52466`. Confirm it's a mobile that has WhatsApp. |
| **Postal codes** | Parippally 691574, Kadakkal 691536, Chirayinkeezhu 695304 are my best guess. Kottarakkara, Karunagappalli and Kottiyam came from your own pages. Wrong postcodes weaken local SEO — please check all six. |
| **Kottiyam** | Exists on your Contact page but was missing from the homepage list of centres. Now included everywhere. |
| **Doctor photos** | All five still share one placeholder. |
| **Package prices** | Not published. Buttons say "message us for pricing". |
| **Sunday hours** | Homepage said "All Days 9–7:30", Contact said Sunday 9–1. I used 9–1. Confirm. |

Edit these in `data.py` if you still have the build script, or directly in the
HTML files.


---

## How service availability works

CT is set up as a Parippally-only service. The site handles this automatically:

- The CT card shows an "Available at Parippally" badge
- The CT page says which centre it's at, and lists only Parippally under "Available at"
- Its Book button skips the centre picker and opens Parippally's WhatsApp directly
- CT appears in the service list on the Parippally branch page, and not on the other five
- Only Parippally's structured data tells Google it offers CT

To make another service single-centre, or to add CT at a second centre later, edit
`data.py` and re-run `python3 build.py`. The line looks like:

```python
dict(slug="ct-scan", name="CT Scan", img="ct-scan", at=["parippally"], ...)
```

Add a slug to that list — `at=["parippally", "kottiyam"]` — and everything above
updates itself. Services with no `at` line are available everywhere.

If you'd rather not run the script, you can edit the HTML by hand, but you'd need
to change it in six places, so the script is worth the five minutes.
