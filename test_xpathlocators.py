import pytest
from playwright.sync_api import Page, expect

def test_xpath_locators(page: Page):

    page.goto("https://demowebshop.tricentis.com/")

    # relative XPath
    logo = page.locator("//img[@alt='Tricentis Demo Web Shop']")
    expect(logo).to_be_visible()

    # absolute XPath (not recommended — very brittle)
    expect(page.locator("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[1]/a[1]/img[1]")).to_be_visible()
    page.wait_for_timeout(5000)

    # xpath with contains() for partial match
    
    products = page.locator("//h2//a[contains(@href,'computer')]")
    products_count = products.count()
    print(f"Products with 'computer' in href: {products_count}")
    # click the first match to avoid strict-mode violation when multiple elements match
    building_products = page.locator("//h2//a[starts-with(text(),'Build')]")
    # building_products.first.click()
    building_products_count = building_products.count()
    print(f"Count of building products: {building_products_count}")
    expect(building_products).to_have_count(building_products_count)

    # Get details of the first product whose text contains 'computer' (case-insensitive via translate)
    first_computer_product = page.locator(
        "//h2//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'computer')]"
    ).first
    product_name = first_computer_product.inner_text()
    print(f"\nFirst product containing 'computer': {product_name.strip()}")

    first_computer_product.click()
    page.wait_for_load_state("networkidle")

    # Extract title and price from the product/category detail page
    page_heading = page.locator("//h1").first.inner_text()
    price_locator = page.locator("//*[@itemprop='price'] | //span[contains(@class,'price-value')]").first
    price = price_locator.inner_text() if price_locator.count() > 0 else "N/A"

    print(f"Page heading : {page_heading.strip()}")
    print(f"Price        : {price.strip()}")


def test_products_starting_with_build(page: Page):

    page.goto("https://demowebshop.tricentis.com/")

    # xpath starts-with() to find products whose text begins with 'Build'
    build_products = page.locator("//h2//a[starts-with(text(),'Build')]")
    count = build_products.count()
    print(f"\nProducts starting with 'Build': {count}")

    for i in range(count):
        name = build_products.nth(i).inner_text()
        print(f"  {i + 1}. {name.strip()}")


def test_footer_last_column_links(page: Page):

    page.goto("https://demowebshop.tricentis.com/")

    # last() picks the final column div inside the footer
    last_col_links = page.locator(
        "(//div[contains(@class,'footer-menu-wrapper')]//div[contains(@class,'column')])[last()]//a"
    )
    count = last_col_links.count()
    print(f"\nLinks in last footer column ({count} total):")

    for i in range(count):
        name = last_col_links.nth(i).inner_text()
        print(f"  {i + 1}. {name.strip()}")

    last_link = last_col_links.nth(count - 1).inner_text()
    print(f"\nLast link: {last_link.strip()}")
