"""Buyer-path and layout checks against an existing local Netlify preview."""
import json
import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("BLOOMFIELD_PREVIEW_URL", "http://127.0.0.1:4173")
ARTIFACT_DIR = Path(__file__).resolve().parents[2] / "preview-artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
PROFILES = [
    ("amy-landino", "Amy Landino", "Amy"),
    ("vincenzo-landino", "Vincenzo Landino", "Vincenzo"),
    ("lali-michelsen", "Lali Michelsen", "Lali"),
]
PATHS = ["/", "/talent/"] + [f"/talent/{slug}/" for slug, _, _ in PROFILES]
SIZES = [(320, 800), (360, 800), (390, 844), (768, 1024),
         (1024, 768), (1440, 1000), (1920, 1080)]


def visit(page, path):
    response = page.goto(BASE_URL + path, wait_until="load")
    assert response.status == 200, (path, response.status)
    assert "default-src 'self'" in response.headers.get("content-security-policy", ""), \
        "run checks against Netlify dev so the actual header policy is exercised"
    page.evaluate("document.fonts.ready")
    assert page.get_by_role("main").count() == 1
    assert page.get_by_role("heading", level=1).count() == 1
    assert page.get_by_role("heading", level=1).is_visible()
    assert page.locator("html").get_attribute("lang") == "en"
    ids = page.locator("[id]").evaluate_all("nodes => nodes.map(n => n.id)")
    assert len(ids) == len(set(ids)), "duplicate IDs confuse fragment navigation"
    assert_no_overflow(page, path)
    assert_text_contrast(page, path)



def assert_text_contrast(page, label):
    failures = page.evaluate("""() => {
        const rgb = value => (value.match(/[\d.]+/g) || []).map(Number);
        const lum = color => color.slice(0,3).map(v => v/255)
            .map(v => v <= .04045 ? v/12.92 : ((v+.055)/1.055)**2.4)
            .reduce((sum,v,i) => sum + v*[.2126,.7152,.0722][i],0);
        const background = node => {
            for (let current=node; current; current=current.parentElement) {
                const c=rgb(getComputedStyle(current).backgroundColor);
                if (c.length===3 || c[3]===1) return c;
            }
            return [255,255,255];
        };
        return [...document.querySelectorAll('h1,h2,h3,p,a,.portrait-note,.site-footer>span')]
            .filter(n => n.getClientRects().length && n.textContent.trim()
                && !n.closest('[aria-hidden="true"],.visually-hidden')
                && !n.classList.contains('skip-link'))
            .map(n => {
                const s=getComputedStyle(n), a=lum(rgb(s.color)), b=lum(background(n));
                const ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
                const large=parseFloat(s.fontSize)>=24 || (parseFloat(s.fontSize)>=18.66 && parseInt(s.fontWeight)>=700);
                return {text:n.textContent.trim().slice(0,70),ratio,required:large?3:4.5};
            }).filter(result => result.ratio+.001 < result.required);
    }""")
    assert not failures, f"{label}: text contrast failures: {failures}"


def assert_no_overflow(page, label):
    geometry = page.evaluate("""() => ({
        viewport: document.documentElement.clientWidth,
        width: document.documentElement.scrollWidth,
        offenders: [...document.querySelectorAll('body *')]
            .filter(n => !n.classList.contains('visually-hidden') && n.getClientRects().length)
            .map(n => ({tag:n.tagName, class:n.className,
                left:n.getBoundingClientRect().left, right:n.getBoundingClientRect().right}))
            .filter(n => n.right > document.documentElement.clientWidth + 1 || n.left < -1)
            .slice(0, 8)
    })""")
    assert geometry["width"] <= geometry["viewport"], f"{label}: {geometry}"


def assert_inquiry(url, name):
    parsed = urlparse(url)
    assert parsed.scheme == "mailto"
    assert parsed.path == "hello@getbloomfield.com"
    assert name in parse_qs(parsed.query).get("subject", [""])[0]


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        headless=True,
        executable_path=os.environ.get(
            "BLOOMFIELD_CHROME",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        ),
    )
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    errors, page_errors, failed_requests = [], [], []
    context.on("page", lambda page: page.on(
        "console", lambda message: errors.append(message.text)
        if message.type == "error" else None))
    context.on("page", lambda page: page.on(
        "pageerror", lambda error: page_errors.append(str(error))))
    context.on("requestfailed", lambda request: failed_requests.append(
        {"url": request.url, "failure": request.failure}))
    page = context.new_page()

    # Navigate as a buyer, rather than only examining source attributes.
    for slug, name, short in PROFILES:
        visit(page, "/")
        assert page.get_by_role("link", name=name, exact=True).count() == 0
        page.get_by_role("link", name="Meet the talent", exact=False).click()
        page.wait_for_load_state("load")
        assert urlparse(page.url).path == "/talent/"
        page.get_by_role("link", name=name, exact=True).click()
        page.wait_for_load_state("load")
        assert urlparse(page.url).path == f"/talent/{slug}/"
        assert page.get_by_role("heading", name=name, exact=True).is_visible()
        assert_inquiry(page.get_by_role("link", name=f"Inquire about {short}", exact=False).last.get_attribute("href"), name)
        assert_inquiry(page.get_by_role("link", name="Email Bloomfield", exact=False).get_attribute("href"), name)
        page.get_by_role("link", name="All talent", exact=False).click()
        page.wait_for_load_state("load")
        assert urlparse(page.url).path == "/talent/"
    print("Buyer navigation: 3 profiles and person-specific inquiry subjects passed.", flush=True)

    # Keyboard skip link moves focus to the content; every visible link has a name and a usable hit area.
    page = context.new_page()
    visit(page, "/")
    page.keyboard.press("Tab")
    assert page.locator(".skip-link").evaluate("n => n === document.activeElement")
    assert page.locator(".skip-link").is_visible()
    page.keyboard.press("Enter")
    assert page.get_by_role("main").evaluate("n => n === document.activeElement")
    links = page.get_by_role("link").all()
    for link in links:
        if not link.is_visible() or link.get_attribute("class") == "skip-link":
            continue
        assert link.inner_text().strip() or link.get_attribute("aria-label")
        assert link.bounding_box()["height"] >= 44, link.inner_text()
        link.focus()
        assert link.evaluate("n => getComputedStyle(n).outlineStyle") != "none", link.inner_text()
    print("Keyboard focus, skip link, link names and touch target heights passed.", flush=True)

    # Check every page at the same widths. Screenshots are the changed implementation.
    for width, height in SIZES:
        page.set_viewport_size({"width": width, "height": height})
        for path in PATHS:
            visit(page, path)
            if width in (390, 1440):
                name = "homepage" if path == "/" else path.strip("/").split("/")[-1]
                suffix = "mobile" if width == 390 else "desktop"
                page.screenshot(path=str(ARTIFACT_DIR / f"{name}-{suffix}.png"), full_page=True)
        print(f"Responsive geometry passed: all five pages at {width}px.", flush=True)

    # Text enlargement also checks the combined narrow-screen case from review.
    for width in (320, 390):
        page.set_viewport_size({"width": width, "height": 844})
        for path in PATHS:
            visit(page, path)
            original_heading = page.locator("h1").evaluate("n => parseFloat(getComputedStyle(n).fontSize)")
            page.locator("html").evaluate("n => n.style.fontSize = '200%'")
            assert_no_overflow(page, path + f" at {width}px / 200% text")
            if path in ("/", "/talent/"):
                enlarged_heading = page.locator("h1").evaluate("n => parseFloat(getComputedStyle(n).fontSize)")
                assert enlarged_heading >= original_heading * 1.99, "mobile heading ignores the user's text size"
        print(f"200% text enlargement passed on all five pages at {width}px.", flush=True)

    # Essential content and links must not depend on JavaScript.
    no_js = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
    static = no_js.new_page()
    static.goto(BASE_URL + "/talent/", wait_until="load")
    for _, name, _ in PROFILES:
        assert static.get_by_role("link", name=name, exact=True).is_visible()
    static.get_by_role("link", name="Lali Michelsen", exact=True).click()
    assert static.get_by_role("heading", name="Lali Michelsen", exact=True).is_visible()
    assert_inquiry(static.get_by_role("link", name="Email Bloomfield", exact=False).get_attribute("href"), "Lali Michelsen")
    no_js.close()

    reduced = browser.new_context(reduced_motion="reduce", viewport={"width": 390, "height": 844})
    reduced_page = reduced.new_page()
    for path in PATHS:
        visit(reduced_page, path)
        assert reduced_page.locator("html").evaluate("n => getComputedStyle(n).scrollBehavior") == "auto"
        assert reduced_page.get_by_role("heading", level=1).is_visible()
    reduced.close()
    print("No-JavaScript buyer path and reduced-motion content passed.", flush=True)

    # Request retired paths without rendering their expected 410 console messages.
    retired = context.request.get(BASE_URL + "/manufacturing-ai-guide.html")
    assert retired.status == 410
    assert "This page has been retired." in retired.text()
    assert context.request.get(BASE_URL + "/410.html").status == 410
    for slug, _, _ in PROFILES:
        assert context.request.get(BASE_URL + f"/talent/{slug}").status == 200
    print("Netlify profile URLs and retired-route 410 responses passed.", flush=True)

    assert not errors, f"console errors: {errors}"
    assert not page_errors, f"page errors: {page_errors}"
    assert not failed_requests, f"failed resources: {failed_requests}"
    browser.close()

print(json.dumps({"result": "passed", "screenshots": str(ARTIFACT_DIR),
                  "viewports": [width for width, _ in SIZES], "pages": PATHS}))
