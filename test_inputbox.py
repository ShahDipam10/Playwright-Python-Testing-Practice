import pytest
from playwright.sync_api import Page, expect

def test_inputbox(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")
    text_box = page.locator("#name")

    # visbility check and enable check
    expect(text_box).to_be_visible()
    expect(text_box).to_be_enabled()

    # check the attribute of the elements
    expect(text_box).to_have_attribute("maxlength", "15")

    # get the value of the attribute
    text_box_value = text_box.get_attribute("type")
    print(f"Value of the attribute is: {text_box_value}")

    # pass the value to the input box
    text_box.fill("Dipam Shah")
    text_box_value = text_box.input_value()
    print(f"Value of the input box is: {text_box_value}")

def test_radio_button(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")
    male_radio_button = page.locator("#male")
    female_radio_button = page.locator("#female")

    # visbility check and enable check
    expect(male_radio_button).to_be_visible()
    expect(male_radio_button).to_be_enabled()

    # check the default state of the radio button
    male_radio_button_value = male_radio_button.is_checked()
    print(f"Is the male radio button checked? : {male_radio_button_value}")

    female_radio_button_value = female_radio_button.is_checked()
    print(f"Is the female radio button checked? : {female_radio_button_value}")

    # get the value of the attribute
    male_radio_button_value = male_radio_button.get_attribute("value")
    print(f"Value of the male radio button attribute is: {male_radio_button_value}")

    female_radio_button_value = female_radio_button.get_attribute("value")
    print(f"Value of the female radio button attribute is: {female_radio_button_value}")

    # click on the radio button
    male_radio_button.click()
    male_radio_button_value = male_radio_button.is_checked()
    print(f"Is the male radio button checked? : {male_radio_button_value}")

def test_checkbox(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")
    monday_checkbox = page.locator("#monday")
    tuesday_checkbox = page.locator("#tuesday")
    wednesday_checkbox = page.locator("#wednesday")

    # visibility and enabled checks
    expect(monday_checkbox).to_be_visible()
    expect(monday_checkbox).to_be_enabled()

    # verify all three are unchecked by default
    print(f"Is Monday checked by default? : {monday_checkbox.is_checked()}")
    print(f"Is Tuesday checked by default? : {tuesday_checkbox.is_checked()}")
    print(f"Is Wednesday checked by default? : {wednesday_checkbox.is_checked()}")

    # get the value attribute of a checkbox
    monday_value = monday_checkbox.get_attribute("value")
    print(f"Value attribute of Monday checkbox: {monday_value}")

    # check Monday — unlike radio buttons, multiple checkboxes can be checked at once
    monday_checkbox.check()
    expect(monday_checkbox).to_be_checked()
    print(f"Is Monday checked after .check()? : {monday_checkbox.is_checked()}")

    # check Tuesday as well — Monday stays checked (no mutual exclusion)
    tuesday_checkbox.check()
    expect(tuesday_checkbox).to_be_checked()
    expect(monday_checkbox).to_be_checked()
    print(f"Is Tuesday checked? : {tuesday_checkbox.is_checked()}")
    print(f"Is Monday still checked? : {monday_checkbox.is_checked()}")

    # uncheck Monday — Tuesday should remain checked
    monday_checkbox.uncheck()
    expect(monday_checkbox).not_to_be_checked()
    expect(tuesday_checkbox).to_be_checked()
    print(f"Is Monday unchecked after .uncheck()? : {not monday_checkbox.is_checked()}")
    print(f"Is Tuesday still checked? : {tuesday_checkbox.is_checked()}")

def test_checkbox_select_all(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")

    # all six day checkboxes on the page (Mon–Sat, no Sunday)
    all_day_ids = ["#monday", "#tuesday", "#wednesday", "#thursday", "#friday", "#saturday"]
    checkboxes = [page.locator(id) for id in all_day_ids]

    # verify every checkbox starts unchecked
    for checkbox in checkboxes:
        expect(checkbox).not_to_be_checked()
    print("All checkboxes are unchecked by default")

    # check all checkboxes one by one
    for checkbox in checkboxes:
        checkbox.check()

    # verify every checkbox is now checked
    for checkbox in checkboxes:
        expect(checkbox).to_be_checked()
    print("All checkboxes are now checked")

    # uncheck all checkboxes one by one
    for checkbox in checkboxes:
        checkbox.uncheck()

    # verify every checkbox is unchecked again
    for checkbox in checkboxes:
        expect(checkbox).not_to_be_checked()
    print("All checkboxes are unchecked again")

    # check only the last three (Friday, Saturday, Sunday) using slice [-3:]
    last_three = checkboxes[-3:]
    for checkbox in last_three:
        checkbox.check()

    # verify last three are checked and first four remain unchecked
    for checkbox in last_three:
        expect(checkbox).to_be_checked()
    for checkbox in checkboxes[:-3]:
        expect(checkbox).not_to_be_checked()
    print("Last three (Thursday, Friday, Saturday) are checked; Mon-Wed remain unchecked")


def test_single_selection_dropdown(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")
    country_dropdown = page.locator("#country")

    # visibility and enabled checks
    expect(country_dropdown).to_be_visible()
    expect(country_dropdown).to_be_enabled()

    # count total number of options in the dropdown
    all_options = page.locator("#country option")
    total_options = all_options.count()
    print(f"Total number of options in dropdown: {total_options}")

    # print the default selected value before interaction
    default_value = country_dropdown.input_value()
    print(f"Default selected value: {default_value}")

    # select India by visible label text
    country_dropdown.select_option(label="India")

    # verify India is now selected
    selected_value = country_dropdown.input_value()
    print(f"Selected value after selection: {selected_value}")
    expect(country_dropdown).to_have_value("india")

def test_multi_selection_dropdown(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")

    # ── Colors multi-select ──────────────────────────────────────────────────
    colors_dropdown = page.locator("#colors")

    expect(colors_dropdown).to_be_visible()
    expect(colors_dropdown).to_be_enabled()

    # count total options available
    total_colors = page.locator("#colors option").count()
    print(f"Total color options: {total_colors}")

    # get all available color options and print them sorted alphabetically
    all_color_names = colors_dropdown.evaluate(
        "select => Array.from(select.options).map(o => o.text)"
    )
    print(f"All color options (original order): {all_color_names}")
    print(f"All color options (sorted):         {sorted(all_color_names)}")

    # select multiple colors — passing a list mimics Ctrl+Click selection
    colors_dropdown.select_option(["Red", "Blue", "Green"])

    # verify all three are selected
    selected_colors = colors_dropdown.evaluate(
        "select => Array.from(select.selectedOptions).map(o => o.text)"
    )
    print(f"Selected colors: {selected_colors}")
    assert "Red" in selected_colors
    assert "Blue" in selected_colors
    assert "Green" in selected_colors

    # ── Sorted list multi-select ─────────────────────────────────────────────
    sorted_list = page.get_by_role("listbox", name="Sorted List:")

    expect(sorted_list).to_be_visible()
    expect(sorted_list).to_be_enabled()

    # count total options available
    total_items = sorted_list.locator("option").count()
    print(f"Total sorted list options: {total_items}")

    # get all available sorted list options and print them sorted alphabetically
    all_item_names = sorted_list.evaluate(
        "select => Array.from(select.options).map(o => o.text)"
    )
    print(f"All sorted list options (original order): {all_item_names}")
    print(f"All sorted list options (sorted):         {sorted(all_item_names)}")

    # select multiple items from the sorted list
    sorted_list.select_option(["Cat", "Dog", "Lion"])

    # verify all three are selected
    selected_items = sorted_list.evaluate(
        "select => Array.from(select.selectedOptions).map(o => o.text)"
    )
    print(f"Selected items: {selected_items}")
    assert "Cat" in selected_items
    assert "Dog" in selected_items
    assert "Lion" in selected_items
