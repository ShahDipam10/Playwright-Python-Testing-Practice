"""
FILE: test_example.py
PURPOSE: Introductory Playwright tests — covers page navigation, title/URL assertions,
         role-based locators, and basic interaction (click).

KEY CONCEPTS:
  - `page` is a Playwright fixture automatically provided by pytest-playwright.
    You DON'T create it manually; just declare it as a parameter.
  - `expect(...)` is Playwright's built-in assertion engine (auto-retries until timeout).
  - `re.compile(...)` lets you use regex patterns inside assertions.

HOW TO RUN:
    pytest test_example.py               # run all tests in this file
    pytest test_example.py -v            # verbose output (shows each test name)
    pytest test_example.py --headed      # run with a visible browser window
    pytest test_example.py -k "title"    # run only tests whose name contains "title"
"""

import re
from playwright.sync_api import Page, expect


# ─── TEST 1: Page Title Assertion ──────────────────────────────────────────────
# `expect(page).to_have_title(...)` checks the <title> tag of the page.
# Using re.compile("Playwright") means the title just needs to CONTAIN the word,
# not be an exact match — great when the full title is long or might change.
def test_has_title(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))


# ─── TEST 2: Click & Navigation ────────────────────────────────────────────────
# `page.get_by_role("link", name="...")` finds an <a> tag by its visible text.
# This is the PREFERRED Playwright locator — it mimics how a real user finds things
# (by what they SEE), not by CSS classes or XPaths that break when design changes.
# After click, we assert a heading exists — confirming navigation succeeded.
def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # get_by_role is robust: works even if the HTML structure changes
    page.get_by_role("link", name="Get started").click()

    # to_be_visible() waits (auto-retry) until the heading appears in the DOM
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()


# ─── TEST 3: URL Assertion ─────────────────────────────────────────────────────
# `expect(page).to_have_url(...)` checks the current browser URL.
# Two patterns shown here:
#   1. Exact string match  → checks URL is exactly "https://playwright.dev/"
#   2. Regex match         → checks URL contains "docs/intro" anywhere
def test_verifyPageUrl(page: Page):
    page.goto("https://playwright.dev/")

    # Exact URL check — page must be at this exact address
    expect(page).to_have_url("https://playwright.dev/")

    page.get_by_role("link", name="Get started").click()

    # Regex URL check — useful when query params or hash fragments are unpredictable
    expect(page).to_have_url(re.compile(".*docs/intro"))


# ─── TEST 4: Getting Page Info (title & URL as variables) ─────────────────────
# `page.title()` → returns the page title as a plain Python string (method call).
# `page.url`     → returns the current URL as a plain Python string (property, no ()).
# NOTE: These don't assert anything; they just retrieve values you can print/use.
# In real tests you'd `assert mytitle == "Expected Title"` or use `expect(page)`.
def test_Alianpage(page: Page):
    page.goto("https://aliansoftware.com/")
    mytitle = page.title()          # method — note the ()
    print("The page title is: ", mytitle)
    myurl = page.url                # property — no ()
    print("The page URL is: ", myurl)
