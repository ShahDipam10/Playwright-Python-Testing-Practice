"""
FILE: test_pwlocatorsdemo.py
PURPOSE: Demonstrate all major Playwright built-in locator strategies.

PLAYWRIGHT LOCATOR CHEAT SHEET:
  get_by_alt_text(text)       → finds images/elements by their `alt` attribute
  get_by_text(text)           → finds elements by their visible text content
  get_by_role(role, name=...) → finds elements by ARIA role + accessible name (BEST PRACTICE)
  get_by_placeholder(text)    → finds <input> / <textarea> by placeholder text
  get_by_label(text)          → finds form fields by their associated <label>
  get_by_title(text)          → finds elements by their `title` attribute
  get_by_test_id(id)          → finds elements by `data-testid` attribute (set by devs for testing)
  locator(selector)           → classic CSS / XPath selector (fallback when above don't work)

GOLDEN RULE: Prefer built-in locators (role > label > placeholder > text > testid > alt > title)
             over CSS/XPath. They're more readable, accessible-friendly, and resilient to UI changes.

HOW TO RUN:
    pytest test_pwlocatorsdemo.py -v --headed
"""

import re
from playwright.sync_api import Page, expect


# ─── LOCATOR 1: get_by_alt_text ────────────────────────────────────────────────
# Finds an element whose `alt` attribute matches the given text.
# Most commonly used for <img> tags.
# `exact=True` means the full alt text must match exactly (no partial match).
# Without exact=True, a partial match is also accepted.
def test_verify_pwlocators(page: Page):
    page.goto("https://wattlandscaping.com/")
    page.wait_for_timeout(5000)   # wait 5s for page to fully load (in ms)

    logo = page.get_by_alt_text("Watt Landscaping")   # stores the locator (not yet interacted)
    # logo.click()  ← you COULD click it; here we just assert visibility

    # exact=True → alt must be EXACTLY "Watt Landscaping", not "Watt Landscaping Logo" etc.
    expect(
        page.get_by_alt_text("Watt Landscaping", exact=True)
    ).to_be_visible()

    page.close()


# ─── LOCATOR 2: get_by_text ────────────────────────────────────────────────────
# Finds elements by the visible text they display.
# NOTE: This locator just FINDS the element — it doesn't assert anything here.
# To verify, wrap it in expect(...).to_be_visible() or expect(...).to_have_text(...)
# TIP: Prefer shorter unique substrings over full sentences to avoid brittle tests.
def test_verify_pwlocators2(page: Page):
    page.goto("https://wattlandscaping.com/")
    page.wait_for_timeout(5000)

    # Just locating the element (no assertion here — add expect() to make it a real test)
    page.get_by_text("Professional Landscaping in West Houston, TX | Watt Landscaping")

    page.close()


# ─── LOCATOR 3: get_by_role ────────────────────────────────────────────────────
# Finds elements by their ARIA role and accessible name.
# This is the MOST RECOMMENDED approach in Playwright because:
#   - It aligns with how assistive technologies (screen readers) perceive the page
#   - It's resilient to HTML/CSS changes
# Common roles: "link", "button", "heading", "textbox", "checkbox", "listitem", etc.
def test_verify_pwlocators3(page: Page):
    page.goto("https://wattlandscaping.com/")
    page.wait_for_timeout(5000)

    # Finds the <a> tag with visible text "Contact"
    page.get_by_role("link", name="Contact")
    # NOTE: No assertion here — in a real test you'd click it or assert visibility

    page.close()


# ─── LOCATOR 4: get_by_placeholder ────────────────────────────────────────────
# Finds <input> or <textarea> elements by the `placeholder` attribute.
# Very useful for search boxes, login forms, etc.
# `.fill(text)` clears the field and types the given text into it.
def test_verify_pwlocators4(page: Page):
    page.goto("https://chasseur.com.au/")
    page.wait_for_timeout(5000)

    # Finds the search input and types "French Oven" into it
    page.get_by_placeholder("Search Casseroles Products...").fill("French Oven")

    page.wait_for_timeout(5000)   # wait to see results (use proper wait in production)
    page.close()


# ─── LOCATOR 5: get_by_title ───────────────────────────────────────────────────
# Finds elements by their HTML `title` attribute (tooltip text shown on hover).
# Less common but useful when elements use title for accessibility/description.
# `to_have_text(...)` asserts the element's visible text content equals "Home".
def test_verify_pwlocators5(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")
    page.wait_for_timeout(5000)

    # Both lines target the same element — second one also asserts its text
    page.get_by_title("Home page link")                              # locate (no assertion)
    expect(page.get_by_title("Home page link")).to_have_text("Home") # assert visible text


# ─── LOCATOR 6: get_by_test_id ─────────────────────────────────────────────────
# Finds elements by the `data-testid` attribute (e.g. <div data-testid="profile-name">).
# Developers add these attributes specifically for testing — they don't change with
# design updates, making them the MOST STABLE locator strategy.
# BEST PRACTICE: Ask your dev team to add data-testid to important elements.
def test_verify_pwlocators6(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")
    page.wait_for_timeout(5000)

    expect(page.get_by_test_id("profile-name")).to_have_text("John Doe")
    expect(page.get_by_test_id("profile-name")).to_be_visible()


# ─── LOCATOR 7: locator() with CSS selectors ──────────────────────────────────
# `page.locator(selector)` accepts CSS selectors and XPath.
# Use this as a FALLBACK when the semantic locators above don't work.
#
# CSS examples:
#   "input[name='username']"  → <input> with name attribute = "username"
#   "button[type='submit']"   → <button> with type = "submit"
#   "h6:has-text('Dashboard')"→ <h6> containing text "Dashboard" (Playwright extension)
#
# This test also demonstrates a FULL LOGIN FLOW:
#   1. Navigate to login page
#   2. Fill username
#   3. Fill password
#   4. Click submit
#   5. Assert successful login (Dashboard heading visible)
def test_orangehrm_login(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.wait_for_timeout(5000)

    # CSS selector: input element with name="username"
    page.locator("input[name='username']").fill("Admin")

    # CSS selector: input element with name="password"
    page.locator("input[name='password']").fill("admin123")

    # CSS selector: button element with type="submit"
    page.locator("button[type='submit']").click()

    page.wait_for_timeout(5000)

    # Playwright CSS extension: :has-text() — checks text inside an element
    # This confirms we're on the Dashboard after login
    expect(page.locator("h6:has-text('Dashboard')")).to_be_visible()

    page.close()
