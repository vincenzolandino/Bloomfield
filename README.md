# Bloomfield

Independent creator representation office. Public site for [getbloomfield.com](https://getbloomfield.com/).

## Phase A scope

This branch rebuilds the public website as a **static single-page site**. It is intended to merge through a pull request into `main`.

Phase A does **not**:

- Force-push or orphan-reset `main`
- Delete remote tags or branches
- Change production Netlify settings
- Rewrite git history

A later history-reset / cutover phase (Phase C) is out of scope here.

## What this site is

Bloomfield provides independent representation for internet-native talent. The public page covers representation and career strategy, brand partnerships, commercial development, and deal operations. Every inquiry routes to `hello@getbloomfield.com`.

There is one public landing page (`index.html`) and a branded retired-content page (`410.html`). Former manufacturing, AI consulting, blog, and legal URLs are mapped to HTTP 410.

## Identity rules

Do not publish or imply:

- Fictional employees, agents, founders, or teams
- A current roster
- Brand relationships that do not exist
- Campaign results, testimonials, press, or awards that do not exist
- A public operating-company name

Public sender name is **Bloomfield**. Contact address is **hello@getbloomfield.com**.

## Stack

Static files only. No framework, package manager, build command, CMS, or client-side router.

```
index.html
410.html
assets/css/site.css
assets/js/site.js
assets/media/
_headers
_redirects
robots.txt
sitemap.xml
README.md
```

JavaScript is progressive: the page is readable and usable without it. `prefers-reduced-motion` removes transforms, image drift, and staggered reveals.

## Local preview

No build step. From the repository root:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080/`.

## Contact

hello@getbloomfield.com
