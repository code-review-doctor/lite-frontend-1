from datetime import datetime
from os import path, makedirs, chmod, pardir
from re import search
from time import sleep

from allure import attach, attachment_type
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

now = datetime.now().isoformat()
file_path = path.abspath(path.join(path.dirname(path.abspath(__file__)), pardir))
screen_dir = path.join(file_path, "screenshot", str(now))


def get_current_date_time_string():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")


def get_formatted_date_time_m_d_h_s():
    return datetime.now().strftime("%m%d%H%M%S")


def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length // len(string_to_expand)) + 1))[:length]


def screen_path():
    if not path.exists(screen_dir):
        makedirs(screen_dir)
        chmod(screen_dir, 0o644)
    return screen_dir


def save_screenshot(driver, _):
    driver.get_screenshot_as_file(path.join(screen_path(), now + ".png"))
    attach(
        driver.get_screenshot_as_png(), now, attachment_type=attachment_type.PNG,
    )


def find_element(driver, by_type, locator):
    delay = 2  # seconds
    try:
        return WebDriverWait(driver, delay).until(EC.presence_of_element_located((by_type, locator)))
    except TimeoutException:
        print("element {} was not found".format(locator))


def find_element_by_href(driver, href):
    return driver.find_element_by_css_selector('[href="' + href + '"]')


def is_element_present(driver, how, what):
    """
    Helper method to confirm the presence of an element on page
    :params how: By locator type
    :params what: locator value
    """
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def click(driver, by_type, locator):
    el = find_element(driver, by_type, locator)
    el.click()


def type_text(driver, text, by_type, locator):
    el = find_element(driver, by_type, locator)
    el.click()
    el.send_keys(text)


def get_text(driver, by_type, locator):
    el = find_element(driver, by_type, locator)
    return el.text


def scroll_down_page(driver, x, y):
    driver.execute_script("window.scrollTo(" + str(x) + ", " + str(y) + ")")


def scroll_to_bottom_of_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


def scroll_to_right_of_page(driver):
    driver.execute_script("window.scrollBy(document.body.scrollWidth, 0)")


def highlight(element):
    """
    Highlights (blinks) a Selenium Webdriver element
    """
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)

    original_style = element.get_attribute("style")
    apply_style("background: yellow; border: 2px solid red;")
    sleep(0.8)
    apply_style(original_style)


def get_element_index_by_text(elements, text: str, complete_match=True):
    """
    Loops through the list of elements, checks if the text is equal or in
    text and returns the index of it if so
    """
    for i in range(0, len(elements)):
        if complete_match:
            if elements[i].text == text:
                return i
        else:
            if text in elements[i].text:
                return i
    return -1


def scroll_to_element_by_id(driver, element_id):
    driver.execute_script("document.getElementById('" + element_id + "').scrollIntoView(true);")


def search_for_correct_date_regex_in_element(element):
    return search(
        "([0-9]{1,2}):([0-9]{2})(am|pm) ([0-9][0-9]) (January|February|March|April|May|June|July|August|September|October|November|December) ([0-9]{4,})",
        element,
    )


def get_formatted_date_time_h_m_pm_d_m_y():
    time = datetime.now().strftime("%I:%M%p %d %B %Y").replace("PM", "pm").replace("AM", "am")
    if time[0] == "0":
        time = time[1:]
    return time


def get_unformatted_date_time():
    return datetime.now()


def get_formatted_date_time_d_h_m_s():
    return datetime.now().strftime(" %d%H%M%S")


def page_is_ready(driver):
    return driver.execute_script("return document.readyState") == "complete"


def menu_is_visible(driver):
    return driver.find_element_by_css_selector(".lite-menu--visible").is_displayed()


def select_visible_text_from_dropdown(element, text):
    select = Select(element)
    select.select_by_visible_text(text)


def find_paginated_item(id, driver):
    driver.set_timeout_to(0)
    current_page = 1
    while True:
        template = driver.find_elements_by_id(id)
        if template:
            element = template[0]
            break
        else:
            current_page += 1
            driver.find_element_by_id(f"page-{current_page}").click()
    driver.set_timeout_to(10)
    assert element, f"Item couldn't be found across {current_page} pages"
    return element


def paginated_search(driver, func: callable):
    """
    Calls a given function on every page until the function returns true or we run out of pages.
    This is useful if you want to run a custom check for element(s) across a paginated page
    """
    driver.set_timeout_to(0)
    success = False
    current_page = 1
    while True:
        result = func
        if result:
            success = True
            break
        else:
            current_page += 1
            driver.find_element_by_id(f"page-{current_page}").click()
    driver.set_timeout_to(10)
    return success


def get_text_of_multi_page_table(css_selector, driver):
    driver.set_timeout_to(0)
    text = ""
    current_page = 1
    while True:
        text += driver.find_element_by_css_selector(css_selector).text
        current_page += 1
        try:
            driver.find_element_by_id(f"page-{current_page}").click()
        except NoSuchElementException:
            break
    driver.set_timeout_to(10)
    return text


def strip_special_characters(string):
    return "".join(e for e in string if e.isalnum())


def get_current_date_time(format_date_time=True):
    date_time = datetime.now()
    if not format_date_time:
        return date_time
    return strip_special_characters(str(date_time))
