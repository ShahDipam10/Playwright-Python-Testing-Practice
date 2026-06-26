"""
FILE: test_assignment.py
PURPOSE: Assignment using https://demowebshop.tricentis.com/

HOW TO RUN:
    pytest test_assignment.py -v --headed -s
    # -s flag is needed to see print() output
"""

from playwright.sync_api import Page, expect

N = 2  # change this to print the Nth product / Nth footer link


def test_logo_and_computers(page: Page):
    page.goto("https://demowebshop.tricentis.com/")

    # Task 2: verify logo visibility
    # actual HTML: <img alt="Tricentis Demo Web Shop" ...> — no class/id on the logo
    logo = page.locator("img[alt='Tricentis Demo Web Shop']")
    expect(logo).to_be_visible()
    print("\nLogo is visible")

    # Navigate to Computers → Desktops
    page.get_by_role("link", name="Computers").first.click()
    page.get_by_role("link", name="Desktops").first.click()

    # Task 3: capture all products and verify count
    # actual site has 6 products in Desktops
    products = page.locator(".product-title a")
    print(f"Product count: {products.count()}")
    expect(products).to_have_count(6)

    all_names = products.all_text_contents()

    # Task 4: first product
    print(f"First product : {all_names[0]}")

    # Task 5: last product
    print(f"Last product  : {all_names[-1]}")

    # Task 6: nth product
    print(f"{N}nd product   : {all_names[N - 1]}")

    # Task 7: all product titles using all_text_contents()
    print("All products  :", all_names)


def test_footer_links(page: Page):
    page.goto("https://demowebshop.tricentis.com/")

    # Task 8: first, last, and nth footer link
    footer_links = page.locator(".footer a")

    print(f"\nFirst footer link : {footer_links.first.text_content()}")
    print(f"Last footer link  : {footer_links.last.text_content()}")
    print(f"{N}nd footer link   : {footer_links.nth(N - 1).text_content()}")
