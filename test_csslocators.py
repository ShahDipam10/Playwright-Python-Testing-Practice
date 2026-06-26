"""
FILE: test_csslocators.py
PURPOSE: Learn CSS selector syntax used inside page.locator() in Playwright.

CSS SELECTOR CHEAT SHEET:
  Syntax                              Example
  ─────────────────────────────────   ──────────────────────────────────────────
  tag                                 input
  #id                                 #small-searchterms
  tag#id                              input#small-searchterms
  .class                              .search-box-text
  tag.class                           input.search-box-text
  [attribute='value']                 [name='q']
  tag[attribute='value']              input[name='q']
  tag.class[attribute='value']        input.search-box-text[value='Search store']
  .class[attribute='value']           .search-box-text[value='Search store']

KEY RULE:
  - `#id` is globally unique, so you can skip the tag name → just use `#small-searchterms`
  - Class names may repeat across many elements, so combine with tag or attribute to be specific
  - Combining class + attribute is the most precise CSS locator pattern

WHEN TO USE CSS vs PLAYWRIGHT BUILT-INS:
  Use CSS (locator()) when no Playwright built-in fits (get_by_role, get_by_placeholder, etc.)
  CSS is a powerful fallback but less readable — prefer semantic locators where possible.

HOW TO RUN:
    pytest test_csslocators.py -v --headed
"""

import pytest
from playwright.sync_api import Page, expect


def test_verify_css_locators(page: Page):
    page.goto("https://demowebshop.tricentis.com/")

    # ── Selector 1: tag + id ──────────────────────────────────────────────────
    # HTML: <input id="small-searchterms" ... />
    # Full form:  "input#small-searchterms"  (tag + id)
    # Short form: "#small-searchterms"        (id alone — always unique, tag optional)
    # page.locator("input#small-searchterms").fill("T-Shirts")
    # page.locator("#small-searchterms").fill("T-Shirts")
    # page.wait_for_timeout(5000)

    # ── Selector 2: tag + class ───────────────────────────────────────────────
    # HTML: <input class="search-box-text" ... />
    # Dot (.) prefix denotes a class name.
    # page.locator("input.search-box-text").fill("T-Shirts")
    # page.wait_for_timeout(5000)

    # ── Selector 3: tag + attribute ───────────────────────────────────────────
    # HTML: <input name="q" ... />
    # Square brackets select by any HTML attribute (not just id/class).
    # Full form:  "input[name='q']"   (tag + attribute)
    # Short form: "[name='q']"         (attribute alone — skip tag if unique enough)
    # page.locator("input[name='q']").fill("T-Shirts")
    # page.locator("[name='q']").fill("T-Shirts")
    # page.wait_for_timeout(5000)

    # ── Selector 4: class + attribute (MOST SPECIFIC) ─────────────────────────
    # HTML: <input class="search-box-text" value="Search store" ... />
    # Combining class AND attribute narrows down to exactly one element.
    # Full form:  "input.search-box-text[value='Search store']"
    # Short form: ".search-box-text[value='Search store']"   ← currently active
    # page.locator("input.search-box-text[value='Search store']").fill("T-Shirts")
    page.locator(".search-box-text[value='Search store']").fill("T-Shirts")



    page.wait_for_timeout(5000)
