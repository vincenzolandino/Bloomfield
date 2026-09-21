# Bloomfield Creator Agency Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace getbloomfield.com and its reachable repository history with a single-page independent creator representation website.

**Architecture:** Build a dependency-free static site from one HTML document, one stylesheet, and one progressive JavaScript file. Netlify serves the root page, applies restrictive headers, and returns HTTP 410 for every retired route while preserving required assets and indexing files.

**Tech Stack:** HTML5, CSS, browser JavaScript, Node.js built-in test runner, Netlify static hosting

**Spec:** `docs/superpowers/specs/2026-09-20-bloomfield-creator-agency-rebuild-design.md`

## Global Constraints

- Public brand name: Bloomfield.
- Public contact address: `hello@getbloomfield.com`.
- Public sender name: Bloomfield.
- One public landing page and one branded retired-content response.
- No invented staff, roster, clients, partnerships, results, testimonials, press, awards, or social profiles.
- No public operating-company name.
- Display font: Bodoni Moda.
- Interface and body font: Familjen Grotesk.
- Colors: ink `#0A0A0A`, warm paper `#F1ECE2`, vermilion `#FF4A2D`, muted paper `#C9C2B6`.
- No framework, CMS, database, client-side router, analytics, advertising scripts, or runtime dependency.
- The page and email action must work without JavaScript.
- All retired public routes must return HTTP 410 after deployment.
- Final remote history contains one clean root commit, one branch named `main`, and no tags.

---

### Task 1: Create the Clean Branch and Site Contract

**Files:**
- Restore: `docs/superpowers/specs/2026-09-20-bloomfield-creator-agency-rebuild-design.md`
- Restore: `docs/superpowers/plans/2026-09-20-bloomfield-creator-agency-rebuild.md`
- Create: `tests/site.test.mjs`

**Interfaces:**
- Consumes: approved design spec and this plan from the existing local `main` branch
- Produces: orphan branch `clean-main` and a Node test contract for all site files

- [ ] **Step 1: Create the orphan branch and restore only approved documentation**

Run:

```bash
git switch --orphan clean-main
git restore --source=main -- docs/superpowers/specs/2026-09-20-bloomfield-creator-agency-rebuild-design.md
git restore --source=main -- docs/superpowers/plans/2026-09-20-bloomfield-creator-agency-rebuild.md
```

Expected: `git status --short` lists only the two documentation files and no legacy files.

- [ ] **Step 2: Write the failing site contract**

Create `tests/site.test.mjs` with Node's built-in `node:test`, `node:assert/strict`, and `node:fs/promises`. The tests must assert:

```js
const requiredFiles = [
  'index.html',
  '410.html',
  'assets/css/site.css',
  'assets/js/site.js',
  '_headers',
  '_redirects',
  'robots.txt',
  'sitemap.xml',
];

const requiredCopy = [
  'Independent representation for internet-native talent.',
  'Representation and career strategy',
  'Brand partnerships',
  'Commercial development',
  'Deal operations',
  'hello@getbloomfield.com',
];

const forbiddenClaims = [
  /our clients/i,
  /our roster/i,
  /our team/i,
  /trusted by/i,
  /award-winning/i,
];
```

Implement these exact assertions after reading `index.html` into `html`:

```js
test('all required files exist', async () => {
  await Promise.all(requiredFiles.map((file) => access(file)));
});

test('the page has one heading and all approved copy', () => {
  assert.equal((html.match(/<h1\b/g) || []).length, 1);
  requiredCopy.forEach((copy) => assert.match(html, new RegExp(escapeRegExp(copy), 'i')));
});

test('the page exposes the approved contact route', () => {
  assert.match(html, /href="mailto:hello@getbloomfield\.com"/i);
});

test('the page contains no unsupported claims', () => {
  forbiddenClaims.forEach((claim) => assert.doesNotMatch(html, claim));
});

test('metadata identifies the canonical organization', () => {
  assert.match(html, /<link rel="canonical" href="https:\/\/getbloomfield\.com\/">/i);
  assert.match(html, /property="og:title"/i);
  assert.match(html, /"@type":\s*"Organization"/i);
});

test('runtime resources stay local', () => {
  assert.match(html, /href="\/assets\/css\/site\.css"/i);
  assert.match(html, /src="\/assets\/js\/site\.js"/i);
  assert.doesNotMatch(html, /<script[^>]+src="https?:/i);
});
```

- [ ] **Step 3: Run the contract to verify it fails**

Run:

```bash
node --test tests/site.test.mjs
```

Expected: FAIL because `index.html` and the remaining required files do not exist.

- [ ] **Step 4: Commit the test contract**

Run:

```bash
git add docs tests/site.test.mjs
git commit -m "test: define Bloomfield site contract"
```

Expected: the orphan branch receives its first root commit.

---

### Task 2: Build the Semantic Landing Page

**Files:**
- Create: `index.html`
- Create: `410.html`
- Create: `assets/media/social-card.svg`
- Modify: `tests/site.test.mjs`

**Interfaces:**
- Consumes: selectors `.site-header`, `.hero`, `.point-of-view`, `.capabilities`, `.focus`, `.process`, `.contact`, and `.site-footer`
- Produces: the complete page structure and copy consumed by `assets/css/site.css` and `assets/js/site.js`

- [ ] **Step 1: Extend the failing contract for semantic structure**

Add assertions that `index.html` contains:

```js
const requiredLandmarks = [
  '<header',
  '<main',
  '<footer',
  'id="point-of-view"',
  'id="capabilities"',
  'id="focus"',
  'id="process"',
  'id="contact"',
];
```

Assert that every capability heading and every process heading from the spec appears once. Assert that the page contains no `<form>`, cookie banner, analytics host, third-party script, or invented social link.

- [ ] **Step 2: Run the semantic contract to verify it fails**

Run:

```bash
node --test tests/site.test.mjs
```

Expected: FAIL on missing semantic landmarks.

- [ ] **Step 3: Implement the page document**

Create `index.html` with this structure:

```html
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <a class="wordmark" href="#top" aria-label="Bloomfield home">Bloomfield</a>
    <a class="header-contact" href="mailto:hello@getbloomfield.com">Contact</a>
  </header>
  <main id="main">
    <section class="hero" id="top">
      <p>Representation / Partnerships / Strategy</p>
      <h1>Independent representation for internet-native talent.</h1>
      <p>Bloomfield handles partnerships, positioning, negotiations, and the business behind the work.</p>
      <a href="mailto:hello@getbloomfield.com">Start a conversation</a>
      <div class="editorial-stage" aria-hidden="true"></div>
    </section>
    <section class="point-of-view" id="point-of-view">
      <h2>Careers need structure.</h2>
      <p>An audience can open a door. A career needs structure. Bloomfield manages the commercial work around the creative work, from the first conversation through signed agreement and final delivery.</p>
    </section>
    <section class="capabilities" id="capabilities">
      <h2>What Bloomfield handles</h2>
      <article><h3>Representation and career strategy</h3></article>
      <article><h3>Brand partnerships</h3></article>
      <article><h3>Commercial development</h3></article>
      <article><h3>Deal operations</h3></article>
    </section>
    <section class="focus" id="focus">
      <h2>Focus</h2>
      <p>Creators / Podcasters / Founders / Athletes / Digital personalities</p>
    </section>
    <section class="process" id="process">
      <h2>How Bloomfield works</h2>
      <article><h3>Position</h3></article>
      <article><h3>Partner</h3></article>
      <article><h3>Manage</h3></article>
    </section>
    <section class="contact" id="contact">
      <h2>Make the introduction.</h2>
      <p>Talent, brands, and collaborators can reach Bloomfield directly.</p>
      <a href="mailto:hello@getbloomfield.com">hello@getbloomfield.com</a>
    </section>
  </main>
  <footer class="site-footer"><span>Bloomfield</span><span>Connecticut, USA</span><span>© 2026 Bloomfield</span></footer>
  <script src="/assets/js/site.js" defer></script>
</body>
```

Use the approved copy verbatim from sections 4.1 through 4.6 of the spec. Add a decorative editorial stage inside the hero using layered `<div>` elements with `aria-hidden="true"`; do not add talent portraits or implied client work.

Set:

```html
<title>Bloomfield | Independent Creator Representation</title>
<meta name="description" content="Bloomfield provides independent representation, brand partnerships, commercial strategy, and deal operations for internet-native talent.">
<link rel="canonical" href="https://getbloomfield.com/">
```

Add matching Open Graph metadata and `Organization` plus `WebSite` JSON-LD. Set the social preview to `https://getbloomfield.com/assets/media/social-card.svg`.

- [ ] **Step 4: Implement the branded retired-content document**

Create `410.html` with the Bloomfield wordmark, the line `This page has been retired.`, a link to `/`, and the same font imports and stylesheet as the landing page.

- [ ] **Step 5: Create the social preview**

Create `assets/media/social-card.svg` at 1200 by 630 pixels using the approved ink, paper, and vermilion colors. Include only the Bloomfield wordmark and `Independent representation for internet-native talent.`

- [ ] **Step 6: Run the contract**

Run:

```bash
node --test tests/site.test.mjs
```

Expected: remaining failures are limited to the missing stylesheet, JavaScript, headers, redirects, and indexing files.

- [ ] **Step 7: Commit the semantic site**

Run:

```bash
git add index.html 410.html assets/media/social-card.svg tests/site.test.mjs
git commit -m "feat: add Bloomfield creator representation page"
```

---

### Task 3: Implement the Editorial Visual System and Motion

**Files:**
- Create: `assets/css/site.css`
- Create: `assets/js/site.js`
- Modify: `tests/site.test.mjs`

**Interfaces:**
- Consumes: semantic selectors from `index.html`
- Produces: `.is-visible` reveal state and CSS custom properties `--ink`, `--paper`, `--accent`, `--muted`, and `--progress`

- [ ] **Step 1: Add failing visual-system tests**

Assert the stylesheet contains:

```js
const requiredCss = [
  '--ink: #0A0A0A',
  '--paper: #F1ECE2',
  '--accent: #FF4A2D',
  '--muted: #C9C2B6',
  '@media (prefers-reduced-motion: reduce)',
  ':focus-visible',
  '@media (max-width: 768px)',
];
```

Assert `site.js` contains `IntersectionObserver`, a reduced-motion query, and no network requests, timers longer than one second, or third-party imports.

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
node --test tests/site.test.mjs
```

Expected: FAIL because the visual files do not exist.

- [ ] **Step 3: Implement the stylesheet**

Create `assets/css/site.css` with:

- A reset and the four approved custom properties.
- Google Fonts imports for Bodoni Moda and Familjen Grotesk.
- A fixed header with a paper-to-transparent blend treatment.
- A hero sized to at least `100svh` with an oversized display headline.
- A CSS editorial stage built from cropped panels, grain, scan lines, and vermilion geometry.
- A two-column point-of-view section.
- Capability rows with large sequence numbers and border transitions.
- A horizontally animated focus rail.
- A three-column process section that collapses cleanly on mobile.
- An ink contact section with one paper-colored email action.
- Visible keyboard focus and 44 pixel minimum action targets.
- Breakpoints at 1024, 768, and 480 pixels.
- A reduced-motion block that disables animation, smooth scrolling, transforms, and transition delays.

- [ ] **Step 4: Implement progressive motion**

Create `assets/js/site.js` as a strict, dependency-free script:

```js
(() => {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll('[data-reveal]');

  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.16 });

  revealItems.forEach((item) => observer.observe(item));
})();
```

- [ ] **Step 5: Run the contract**

Run:

```bash
node --test tests/site.test.mjs
```

Expected: remaining failures concern only Netlify and indexing files.

- [ ] **Step 6: Commit the visual system**

Run:

```bash
git add assets/css/site.css assets/js/site.js tests/site.test.mjs
git commit -m "feat: add editorial design system and motion"
```

---

### Task 4: Configure Netlify, Indexing, and Retired Routes

**Files:**
- Create: `_headers`
- Create: `_redirects`
- Create: `robots.txt`
- Create: `sitemap.xml`
- Modify: `tests/site.test.mjs`

**Interfaces:**
- Consumes: root files and `/assets/*`
- Produces: Netlify response rules and search-engine discovery files

- [ ] **Step 1: Add failing hosting tests**

Assert `_headers` contains CSP, HSTS, `nosniff`, frame protection, referrer policy, and permissions policy. Assert `_redirects` explicitly preserves `/`, `/index.html`, `/410.html`, `/assets/*`, `/robots.txt`, and `/sitemap.xml` before a catch-all 410 rule.

Assert `robots.txt` allows `/` and references `https://getbloomfield.com/sitemap.xml`. Assert the sitemap contains only `https://getbloomfield.com/`.

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
node --test tests/site.test.mjs
```

Expected: FAIL on missing hosting files.

- [ ] **Step 3: Implement security headers**

Create `_headers` with a site-wide block and immutable cache rules for `/assets/*`. The CSP must allow only self-hosted resources plus `https://fonts.googleapis.com` for styles and `https://fonts.gstatic.com` for fonts. Scripts use `'self'` only.

- [ ] **Step 4: Implement route retirement**

Create `_redirects` in this order:

```text
/ /index.html 200
/index.html /index.html 200
/410.html /410.html 410
/assets/* /assets/:splat 200
/robots.txt /robots.txt 200
/sitemap.xml /sitemap.xml 200
/* /410.html 410
```

Validate this behavior in a Netlify-compatible local or deployed environment before declaring success.

- [ ] **Step 5: Add indexing files**

Create `robots.txt`:

```text
User-agent: *
Allow: /
Sitemap: https://getbloomfield.com/sitemap.xml
```

Create a standards-compliant `sitemap.xml` containing only the canonical root URL and the implementation date.

- [ ] **Step 6: Run the complete contract**

Run:

```bash
node --test tests/site.test.mjs
```

Expected: all tests PASS.

- [ ] **Step 7: Commit hosting configuration**

Run:

```bash
git add _headers _redirects robots.txt sitemap.xml tests/site.test.mjs
git commit -m "feat: configure secure Netlify delivery"
```

---

### Task 5: Perform Browser and Repository Verification

**Files:**
- Modify only if verification finds a defect: site files from Tasks 2 through 4

**Interfaces:**
- Consumes: complete `clean-main` tree
- Produces: verified local candidate ready for the remote history replacement

- [ ] **Step 1: Run automated tests and repository checks**

Run:

```bash
node --test tests/site.test.mjs
git diff --check
git status --short
git ls-tree -r --name-only HEAD
```

Expected: tests pass, no whitespace errors, clean status, and only approved site, test, and documentation files appear.

- [ ] **Step 2: Scan the complete tree for prohibited legacy material**

Run a case-insensitive `rg` scan against the entire tracked tree using the known legacy brand vocabulary held outside the repository. Also scan for invented staff names, client claims, roster claims, analytics IDs, and external scripts.

Expected: no prohibited matches.

- [ ] **Step 3: Serve the site locally**

Run:

```bash
python3 -m http.server 4173
```

Expected: the server listens on `http://127.0.0.1:4173`.

- [ ] **Step 4: Verify the page in a browser**

Check desktop and mobile widths for:

- Complete hero and contact visibility
- No horizontal overflow
- Legible type and sufficient contrast
- Working header and email actions
- Visible keyboard focus
- Clean reduced-motion rendering
- No browser console errors

- [ ] **Step 5: Correct defects and rerun verification**

For every defect, add or strengthen an automated assertion where practical, make the smallest correction, rerun `node --test tests/site.test.mjs`, and repeat the affected browser check.

- [ ] **Step 6: Commit verified corrections**

Run only if verification changed files:

```bash
git add index.html 410.html assets _headers _redirects robots.txt sitemap.xml tests
git commit -m "fix: resolve predeployment verification findings"
```

---

### Task 6: Replace Remote History and Verify Production

**Files:**
- No new files

**Interfaces:**
- Consumes: verified `clean-main` branch
- Produces: remote `main`, Netlify deployment, and live getbloomfield.com site

- [ ] **Step 1: Record the current remote state outside the repository**

Run read-only commands to record the current `origin/main` SHA, branch list, tag list, and live response headers in the task log. Do not create a backup branch or tag.

- [ ] **Step 2: Confirm the candidate one final time**

Run:

```bash
node --test tests/site.test.mjs
git status --short
git log --oneline --decorate --max-count=10
```

Expected: tests pass, status is clean, and `clean-main` contains only clean-root history.

- [ ] **Step 3: Replace remote `main`**

Run:

```bash
git push origin clean-main:main --force
```

Expected: GitHub accepts the forced update and reports `main` at the clean-root history.

- [ ] **Step 4: Remove every other remote branch and tag**

List remote references, delete every remote branch except `main`, and delete every remote tag. The current audit found only `main`, so this step should be a no-op unless new references appeared.

- [ ] **Step 5: Verify GitHub from a fresh clone**

Clone `vincenzolandino/Bloomfield` into a new temporary directory. Confirm:

```bash
git branch -a
git tag
git log --oneline --all
git ls-tree -r --name-only HEAD
```

Expected: one branch named `main`, no tags, clean-root history only, and approved files only.

- [ ] **Step 6: Wait for Netlify and verify production**

Poll the live root at reasonable intervals for the new page title. Once deployed, verify:

```bash
curl -sSIL https://getbloomfield.com/
curl -sSIL https://getbloomfield.com/a-retired-path
```

Expected: root returns HTTP 200 with the approved security headers. The retired path returns HTTP 410.

- [ ] **Step 7: Run live browser checks**

Open the live site at desktop and mobile widths. Confirm the approved design, functional email links, no overflow, no console errors, and no legacy content.

- [ ] **Step 8: Report deployment evidence**

Report the new remote commit SHA, live URL, automated test result, production status codes, and any hosting caveat discovered during verification.
