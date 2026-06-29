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
