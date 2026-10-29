# Bloomfield Talent Preview Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan inline. Steps use checkbox syntax for tracking.

**Goal:** Build a local buyer-facing homepage, separate Talent index and three specific talent profiles for Dana's review.

**Architecture:** Keep hand-authored static HTML, shared CSS and minimal JavaScript. Store source documents and review screenshots outside the public repository. Preserve the current Netlify site and inquiry inbox.

**Tech Stack:** HTML, CSS, dependency-free JavaScript, Node's test runner, existing Python Playwright and Netlify CLI.

**Spec:** `docs/superpowers/specs/2026-10-29-bloomfield-talent-preview.md`

## Global Constraints

- Local branch `codex/bloomfield-talent-refresh`; no push or deploy.
- No new dependencies, services, paid assets or persistent permissions.
- Keep agency leadership unnamed in public copy and metadata; Vincenzo is represented talent.
- Use the reviewed headline and inquiry copy; put the roster on /talent/ only. Preserve `hello@getbloomfield.com`.
- Real portraits remain pending. Use clearly marked preview frames, never fabricated faces.
- Public proof only; no private fees, internal prospect lists or strategy text.
- No em dashes, inflated claims or agency slogans in website copy.

## Review Focus

- A buyer arriving directly on any profile can reach the inbox with the right person's name in the subject.
- The roster and profile content remain usable with JavaScript disabled or motion reduced.
- Long names, three-line headings and inquiry addresses fit at 320px and 200% text zoom.
- All page links and local assets resolve, including Netlify's pretty URLs and retired paths.
- Header policy matches inline metadata and permits approved local media without opening external resource access.

### Task 1: Buyer paths and page content

**Files:** Modify `index.html`, `assets/css/site.css`, `assets/js/site.js`, `410.html`, `tests/site.test.mjs` and `tests/browser_check.py`. Create `talent/index.html`, `talent/amy-landino/index.html`, `talent/vincenzo-landino/index.html` and `talent/lali-michelsen/index.html`.

**Interfaces:** The homepage links to `/talent/`. That index links to `/talent/amy-landino/`, `/talent/vincenzo-landino/` and `/talent/lali-michelsen/`. Each page uses `mailto:hello@getbloomfield.com` with a person-specific subject. All pages use `/assets/css/site.css?v=20261029` and `/assets/js/site.js?v=20261029`.

- [ ] Replace obsolete wording tests with checks for valid metadata, reachable local links and assets, and intact CSP script hashes. Update the browser check to navigate all three cards to the correct profile and inspect the inquiry target.
- [ ] Run the new checks against the existing site. Expected: missing-profile and buyer-path failures.
- [ ] Build the reviewed homepage and three distinct profiles. Use portrait frames and verified public proof links; omit unsupported credits. Keep all content visible without animation or JavaScript.
- [ ] Run the Node suite and browser buyer-path checks. Expected: every profile loads, all inquiries reach the same inbox with the correct subject, local links and assets exist.

### Task 2: Routing, metadata and review assets

**Files:** Modify `_redirects`, `_headers`, `sitemap.xml`, and `assets/media/social-card.svg`. Add a concise public implementation note under `docs/` with source URLs and remaining portrait requirements.

**Interfaces:** Explicit profile routes return 200; legacy routes still return 410. The sitemap lists the homepage, Talent index and three profiles. CSP hashes correspond to each inline schema block; CSS/JS have versioned references.

- [ ] Add checks for the three canonical profile paths in routing and sitemap, and validate each inline schema script against the actual header policy.
- [ ] Run the checks. Expected: missing routes and schema mismatch fail until configured.
- [ ] Update Netlify routing, metadata, indexing and the share artwork without broadening media permissions.
- [ ] Run `node --test tests/site.test.mjs` and `node --check assets/js/site.js`. Expected: all pass.

### Task 3: Browser verification and handoff

**Files:** `tests/browser_check.py`; local screenshots and a review report outside the public repository.

**Interfaces:** Run a local Netlify preview on port 4173. Screenshots are written to `../preview-artifacts/`; no remote deployment is involved.

- [ ] Verify desktop/mobile pages, keyboard focus, card navigation, inquiry URLs, local resources, retired paths, no-JavaScript content and reduced motion. Wait for fonts before geometry assertions.
- [ ] Review desktop and mobile screenshots. Correct layout defects and rerun only affected checks, then the final suite.
- [ ] Review the whole diff, document missing portraits and any verification limits, and commit the local preview after checks pass. Send the local preview and screenshots to the coordinating thread for Dana's review.

The coordinating thread has already authorized this local implementation after Dana's copy review. No additional execution-method approval is required. Final copy and asset approval, pushing, and deployment remain outside this plan.
