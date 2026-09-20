# Launching the website — step by step

Written for someone who has never used GitHub. Nothing here needs the command
line. Everything happens in a web browser.

**Total time:** about 40 minutes of work, then a few hours of waiting.

---

## Read this first

Your website is live right now on whatever hosting you have. This guide moves it
to GitHub. Two rules:

1. **Do not cancel your current hosting yet.** Wait a week after the new site is
   working. If something goes wrong you want somewhere to fall back to.
2. **Back up your current site first.** Log in to your existing hosting control
   panel, find `public_html`, select everything, compress it, and download the
   zip. Keep it somewhere safe.

The good news: the domain stays yours at GoDaddy throughout. We're only changing
where it points.

---

## Part 1 — Create a GitHub account

**Skip if you already have one.**

1. Go to **github.com**
2. Click **Sign up**
3. Enter your email, create a password, pick a username

   Your username becomes part of a web address, so choose something sensible —
   `doctorsscans` rather than a nickname. If it's taken, try `doctorsscanslabs`.
4. Verify your email when GitHub sends the code
5. When asked which plan, choose **Free**

Write down your username. You'll need it later, and I'll call it
**YOUR-USERNAME** for the rest of this guide.

---

## Part 2 — Create the repository

A repository, or "repo", is just a folder that lives on GitHub.

1. Once logged in, click the **+** in the top-right corner → **New repository**
2. Fill in:
   - **Repository name:** `doctorsscans-website`
   - **Description:** optional, leave blank
   - Select **Public**

     It must be public for free GitHub Pages hosting. That's fine — your website
     is public anyway. Nothing private is in these files.
   - Do **not** tick "Add a README file"
3. Click **Create repository**

You'll land on a mostly empty page with setup instructions. Ignore all of it.

---

## Part 3 — Upload the website files

1. Unzip `doctorsscans-site.zip` on your computer. You'll get a folder containing
   `index.html`, `assets`, `services`, `branches` and so on.

2. **Open that folder** so you can see what's inside. This matters — you upload
   the *contents*, not the folder itself.

3. On the GitHub page, find the link **uploading an existing file** and click it.
   (If you don't see it: **Add file** → **Upload files**.)

4. **Select everything inside the unzipped folder** and drag it onto the GitHub
   upload area.
   - Windows: click inside the folder, press `Ctrl + A`, drag
   - Mac: click inside the folder, press `Cmd + A`, drag

   GitHub will list the files as it reads them. Wait for it to finish — it takes
   a minute or two.

   **How to check you got everything:** after uploading, your repository should
   show these 12 items at the top level:

   `about` · `assets` · `branches` · `contact` · `doctors` · `packages` ·
   `services` · `404.html` · `CNAME` · `favicon.ico` · `index.html` ·
   `robots.txt` · `sitemap.xml`

   (Plus `_redirects`, `.htaccess`, `README.md` and `LAUNCH-GUIDE.md`, which may
   or may not have come across. None of those four are needed for the site to
   work on GitHub.)

5. Scroll down. In the box under **Commit changes**, type `First upload`.

6. Click **Commit changes**.

You should now see your files listed: `assets`, `branches`, `services`,
`index.html` and the rest.

### Now add one small file by hand

Your computer hides files whose names start with a dot, so one important file
probably didn't upload. Let's create it directly.

1. Click **Add file** → **Create new file**
2. In the filename box, type exactly: `.nojekyll`

   Note the dot at the start. Leave the file content empty.
3. Scroll down, click **Commit changes**

This one empty file tells GitHub to publish your folders exactly as they are.
Without it some pages break.

### Check the CNAME file made it

Look for a file called `CNAME` in the list. If it's there, good. If not:

1. **Add file** → **Create new file**
2. Filename: `CNAME`
3. In the content box, type: `www.doctorsscans.com`
4. **Commit changes**

---

## Part 4 — Turn on GitHub Pages

1. In your repository, click **Settings** (the tab along the top, with the gear)
2. In the left sidebar, scroll down and click **Pages**
3. Under **Build and deployment** → **Source**, choose **Deploy from a branch**
4. Under **Branch**, set the dropdown to **main** and the folder to **/ (root)**
5. Click **Save**

Wait two or three minutes, then refresh the page. A green banner appears with a
web address like:

```
https://YOUR-USERNAME.github.io/doctorsscans-website/
```

**Open it.** Your new website should load.

> Some images or styling may look broken at this address. That's expected and it
> is not a mistake — the site is built for `www.doctorsscans.com`, not a
> sub-folder address. It will look correct once the domain is connected. Check
> that the pages and text are there; don't worry about the layout yet.

---

## Part 5 — Connect your domain in GitHub

Still in **Settings → Pages**:

1. Find the **Custom domain** box
2. Type: `www.doctorsscans.com`
3. Click **Save**

GitHub will show a warning that the domain isn't configured yet. Correct — that's
the next part.

---

## Part 6 — Point the domain at GitHub (GoDaddy)

This is the step that actually moves your website. Take your time.

1. Log in to **godaddy.com**
2. Click your name (top right) → **My Products**
3. Find `doctorsscans.com` → click **DNS** next to it

You'll see a table of DNS records.

### 6a. Note what's there now

**Before changing anything, take a screenshot of the whole table.** If something
goes wrong, this lets you put it back.

### 6b. Change the www record

Find the row where **Type** is `CNAME` and **Name** is `www`.

- Click the pencil / edit icon on that row
- Change **Value** to: `YOUR-USERNAME.github.io`

  Use your actual username. For example if your username is `doctorsscans`, the
  value is `doctorsscans.github.io` — no `https://`, no slash at the end, and
  **not** the repository name.
- **TTL:** 1 hour, or the shortest option offered
- **Save**

If there is no `www` row, click **Add New Record** and create one:
Type `CNAME`, Name `www`, Value `YOUR-USERNAME.github.io`.

### 6c. Change the main domain records

Find rows where **Type** is `A` and **Name** is `@`. Delete every one of them
(the bin icon), then add four new records.

Click **Add New Record** four times, entering:

| Type | Name | Value | TTL |
|---|---|---|---|
| A | @ | `185.199.108.153` | 1 hour |
| A | @ | `185.199.109.153` | 1 hour |
| A | @ | `185.199.110.153` | 1 hour |
| A | @ | `185.199.111.153` | 1 hour |

Yes, all four, all with the name `@`. That's correct — they're GitHub's servers.

These four make `doctorsscans.com` (without the www) work too.

### 6d. Remove anything conflicting

- If there's a **Forwarding** section set up for the domain, turn it off
- Leave MX records alone — those are your email. Deleting them stops your email.

### 6e. Save

GoDaddy may ask you to confirm. Do so.

---

## Part 7 — Wait

DNS changes spread across the internet slowly. Usually 30 minutes to 2 hours,
occasionally up to 24.

While waiting, you can check progress at **dnschecker.org** — enter
`www.doctorsscans.com`, choose **CNAME**, and look for `YOUR-USERNAME.github.io`
appearing in the results.

Don't keep changing settings while waiting. That resets the clock.

---

## Part 8 — Turn on the padlock (HTTPS)

Once the domain works:

1. Go back to **Settings → Pages** in your repository
2. The warning should be gone, replaced by a green tick
3. Tick the box **Enforce HTTPS**

If the box is greyed out with "certificate is being provisioned", GitHub is still
issuing your security certificate. Check again in an hour. It can take up to 24
hours. Come back and tick it — don't skip this, browsers warn visitors on sites
without it.

---

## Part 9 — Check everything works

Open each of these and confirm it loads:

- [ ] `https://www.doctorsscans.com` — homepage, images showing
- [ ] `https://doctorsscans.com` — should jump to the www version
- [ ] `https://www.doctorsscans.com/branches/kottiyam/` — a branch page with its map
- [ ] `https://www.doctorsscans.com/services/ct-scan/` — CT page
- [ ] Tap a green **Book on WhatsApp** button → centre list appears → pick one →
      WhatsApp opens with the message written
- [ ] On the CT page, the Book button goes **straight to Parippally**, no list
- [ ] Padlock icon showing in the address bar
- [ ] Open it on your phone and scroll the whole homepage

Also test one old link still works:
`https://www.doctorsscans.com/Services/Doppler%20Studies/`
should land on the new Doppler page.

---

## Part 10 — Tell Google

Do these in the week after launch. They matter more than anything else on this
list for getting patients.

### Submit your sitemap
1. Go to **search.google.com/search-console**
2. Sign in and select `doctorsscans.com`

   Your verification tag is already in every page, so it should verify itself.
3. Left sidebar → **Sitemaps**
4. Type `sitemap.xml` and click **Submit**

### Point each Business Profile at its own branch page
Open **business.google.com** and for each of your six locations, set the website
field to that branch's page instead of the homepage:

| Branch | Website field |
|---|---|
| Parippally | `https://www.doctorsscans.com/branches/parippally/` |
| Kadakkal | `https://www.doctorsscans.com/branches/kadakkal/` |
| Chirayinkeezhu | `https://www.doctorsscans.com/branches/chirayinkeezhu/` |
| Kottarakkara | `https://www.doctorsscans.com/branches/kottarakkara/` |
| Karunagappalli | `https://www.doctorsscans.com/branches/karunagappalli/` |
| Kottiyam | `https://www.doctorsscans.com/branches/kottiyam/` |

This is the highest-value thing you can do after launch. Each profile then points
to a page with matching address, phone and hours — which is what Google uses to
decide who appears in map results.

While you're there, add CT scan to the services list on the Parippally profile.

---

## Making changes later

To edit any page:

1. Open your repository on GitHub
2. Click through the folders to the file — e.g. `about` → `index.html`
3. Click the **pencil** icon (top right of the file)
4. Edit the text
5. Scroll down → **Commit changes**

Your live site updates in about a minute. There's no separate upload step.

To replace a photo: navigate to `assets/images`, click **Add file** →
**Upload files**, and upload a file with the exact same name. It overwrites the
old one.

If you break something, click the **History** link on any file to see previous
versions and restore one.

---

## If something goes wrong

**Site shows 404 at the github.io address**
Settings → Pages → check Source is "Deploy from a branch", branch is **main**,
folder is **/ (root)**. Also check `index.html` is at the top level of the repo,
not inside a sub-folder. If you see a folder named `doctorsscans.com` in your
repo, you uploaded the folder instead of its contents — delete it and re-upload.

**Styling missing, pages look like plain text**
The `.nojekyll` file is missing, or `assets` didn't upload. Check both are in the
repository.

**"Domain does not resolve to the GitHub Pages server"**
DNS hasn't propagated yet. Wait longer. If it's been over 24 hours, re-check the
www CNAME value at GoDaddy — the most common mistake is putting the repository
name in it. It should be just `YOUR-USERNAME.github.io`.

**Enforce HTTPS is greyed out**
Normal for the first several hours. Check back later.

**Your email stopped working**
You deleted the MX records. Restore them from the screenshot you took in step 6a,
or contact GoDaddy support — they can restore them.

**Everything is broken and you want to undo it**
At GoDaddy, put the DNS records back to what your screenshot shows. Your old
hosting takes over again within a couple of hours. That's why you don't cancel it
yet.
