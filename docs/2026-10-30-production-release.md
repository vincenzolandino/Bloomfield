# Bloomfield production release, October 30, 2026

The owner authorized the refined site to go live before 17:00 UTC. This supersedes the local-only hold recorded in earlier preview notes.

The release removes all pending portrait blocks and uses text-led talent cards and profile introductions. The homepage keeps the roster on the separate Talent page. Public agency leadership remains unnamed, and booking inquiries continue to hello@getbloomfield.com.

Netlify's existing main-branch connection builds the site with `node scripts/build.mjs`. The build copies only 14 public website files into `dist/`; notes, tests, repository state and source documents are excluded.

Before release, all seven Node checks and the browser suite passed against the public build: five pages at seven viewport widths, 200% text, keyboard navigation, person-specific inquiries, no-JavaScript navigation, reduced motion, contrast and retired-route status responses. Desktop and mobile screenshots were inspected.

Previous production reference: commit `ca6c3aad0733306356fccd0533b14c2363adc890`, Netlify deploy `6ab10d6bf80dd60008cc1858`. A recovery can use a new commit reverting the release if needed.

Approved portraits remain a future content enhancement. No placeholders or invented images ship in this release.
