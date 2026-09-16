"""Browser checks for the Night Sky city page against the live dev server.

Requires the Flask app running on http://127.0.0.1:5077 (Chromium via Playwright).
"""

import pytest
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:5077/Boston"


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.mark.parametrize("width", [375, 1280])
def test_no_horizontal_scroll(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900})
    page.goto(URL)
    overflow = page.evaluate(
        "document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    assert not overflow, f"horizontal scroll at {width}px"
    page.close()


def test_fahrenheit_toggle_persists_across_reload(browser):
    page = browser.new_page()
    page.goto(URL)
    hero = page.locator(".temp")
    before = hero.text_content()
    page.get_by_role("button", name="°F").click()
    assert hero.text_content() != before
    assert page.get_by_role("button", name="°F").get_attribute("aria-pressed") == "true"
    page.reload()
    assert hero.text_content() != before
    assert page.get_by_role("button", name="°F").get_attribute("aria-pressed") == "true"
    page.close()


def test_every_icon_has_aria_label(browser):
    page = browser.new_page()
    page.goto(URL)
    labels = page.locator('svg[role="img"]').evaluate_all(
        "els => els.map(e => e.getAttribute('aria-label'))"
    )
    assert labels, "expected at least one condition icon"
    assert all(label and label.strip() for label in labels), labels
    page.close()
