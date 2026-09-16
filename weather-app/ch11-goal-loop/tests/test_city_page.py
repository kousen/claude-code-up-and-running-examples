"""Browser checks for the Night Sky city page, run against the live dev server."""

import urllib.request

import pytest
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:5077/Boston"


def _server_up():
    try:
        return urllib.request.urlopen(URL, timeout=5).status == 200
    except OSError:
        return False


# ponytail: skip rather than fail when the dev server is down so plain `pytest` stays green offline.
pytestmark = pytest.mark.skipif(not _server_up(), reason=f"{URL} is not serving")


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()


@pytest.mark.parametrize("width", [375, 1280])
def test_no_horizontal_scroll(page, width):
    page.set_viewport_size({"width": width, "height": 800})
    page.goto(URL)
    overflow = page.evaluate(
        "document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    assert not overflow


def test_fahrenheit_choice_changes_hero_and_survives_reload(page):
    page.goto(URL)
    hero = page.locator(".temp-value")
    celsius_text = hero.inner_text()
    page.get_by_role("button", name="°F").click()
    fahrenheit_text = hero.inner_text()
    assert fahrenheit_text != celsius_text
    page.reload()
    assert page.locator(".temp-value").inner_text() == fahrenheit_text
    assert page.get_by_role("button", name="°F").get_attribute("aria-pressed") == "true"


def test_every_icon_has_an_aria_label(page):
    page.goto(URL)
    labels = page.locator("svg[role='img']").evaluate_all(
        "els => els.map(el => el.getAttribute('aria-label'))"
    )
    assert labels, "expected at least one condition icon"
    assert all(labels)
