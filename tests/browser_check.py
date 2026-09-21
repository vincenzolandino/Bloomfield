from pathlib import Path
from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:4173"
ARTIFACT_DIR = Path("/tmp/bloomfield-browser-check")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def assert_no_horizontal_overflow(page):
    result = page.evaluate(
        """
        () => ({
          overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
          viewport: document.documentElement.clientWidth,
          documentWidth: document.documentElement.scrollWidth,
          offenders: [...document.querySelectorAll('*')]
            .map(node => ({
              tag: node.tagName,
              className: typeof node.className === 'string' ? node.className : '',
              left: Math.round(node.getBoundingClientRect().left),
              right: Math.round(node.getBoundingClientRect().right),
              width: Math.round(node.getBoundingClientRect().width),
            }))
            .filter(item => item.right > document.documentElement.clientWidth + 1 || item.left < -1)
            .sort((a, b) => b.right - a.right)
            .slice(0, 12),
        })
        """
    )
    assert result["overflow"] is False, f"page has horizontal overflow: {result}"


def assert_page_contract(page):
    page.goto(BASE_URL, wait_until="networkidle")
    assert page.title() == "Bloomfield | Independent Creator Representation"
    assert page.locator("h1").count() == 1
    assert page.locator("h1").is_visible()
    assert page.get_by_text("Independent representation for internet-native talent.").is_visible()
    assert page.locator('a[href^="mailto:hello@getbloomfield.com"]').count() >= 3
    assert_no_horizontal_overflow(page)


def reveal_all_sections(page):
    reveals = page.locator('[data-reveal]')
    for index in range(reveals.count()):
        reveals.nth(index).evaluate(
            "node => node.scrollIntoView({ block: 'center', behavior: 'instant' })"
        )
        page.wait_for_timeout(120)
    page.wait_for_timeout(800)
    hidden_reveals = reveals.evaluate_all(
        "nodes => nodes.filter(node => getComputedStyle(node).opacity !== '1').length"
    )
    assert hidden_reveals == 0, "scroll sequence leaves reveal content hidden"


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        headless=True,
        executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    )
    console_errors = []
    page_errors = []

    desktop = browser.new_page(viewport={"width": 1440, "height": 900})
    desktop.on(
        "console",
        lambda message: console_errors.append(message.text)
        if message.type == "error"
        else None,
    )
    desktop.on("pageerror", lambda error: page_errors.append(str(error)))
    assert_page_contract(desktop)
    desktop.locator(".skip-link").focus()
    assert desktop.locator(".skip-link").is_visible()
    reveal_all_sections(desktop)
    desktop.screenshot(path=ARTIFACT_DIR / "desktop.png", full_page=True)

    mobile = browser.new_page(viewport={"width": 390, "height": 844})
    assert_page_contract(mobile)
    reveal_all_sections(mobile)
    mobile.screenshot(path=ARTIFACT_DIR / "mobile.png", full_page=True)

    for width, height in [(360, 800), (768, 1024), (1024, 768), (1920, 1080)]:
        responsive = browser.new_page(viewport={"width": width, "height": height})
        assert_page_contract(responsive)
        responsive.close()

    reduced = browser.new_page(
        viewport={"width": 1024, "height": 768}, reduced_motion="reduce"
    )
    assert_page_contract(reduced)
    hidden_reveals = reduced.locator('[data-reveal]').evaluate_all(
        "nodes => nodes.filter(node => getComputedStyle(node).opacity !== '1').length"
    )
    assert hidden_reveals == 0, "reduced-motion mode hides reveal content"

    retired = browser.new_page(viewport={"width": 1024, "height": 768})
    retired.goto(f"{BASE_URL}/410.html", wait_until="networkidle")
    assert retired.get_by_text("This page has been retired.").is_visible()
    assert retired.locator('a[href="/"]').count() >= 1

    browser.close()

    assert console_errors == [], f"console errors: {console_errors}"
    assert page_errors == [], f"page errors: {page_errors}"

print(f"Browser checks passed. Screenshots: {ARTIFACT_DIR}")
