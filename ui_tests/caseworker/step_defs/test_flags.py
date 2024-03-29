from pytest_bdd import when, then, scenarios, parsers

from ui_tests.caseworker.pages.shared import Shared
from ui_tests.caseworker.pages.add_edit_flag import AddEditFlagPage
from ui_tests.caseworker.pages.advice import FinalAdvicePage
from ui_tests.caseworker.pages.assign_flags_to_case import CaseFlagsPages
from ui_tests.caseworker.pages.case_page import CasePage
from ui_tests.caseworker.pages.flags_list_page import FlagsListPage
import tests_common.tools.helpers as utils
from tests_common import functions


scenarios("../features/flags.feature", strict_gherkin=False)


@when(parsers.parse('I add a new flag with blocking approval set to "{blocks_finalising}"'))
def add_flag(driver, context, blocks_finalising):
    add_edit_flag_page = AddEditFlagPage(driver)
    context.flag_name = f"UAE {utils.get_formatted_date_time_d_h_m_s()}"[:24]

    FlagsListPage(driver).click_add_a_flag_button()

    add_edit_flag_page.enter_name(context.flag_name)
    add_edit_flag_page.select_level("Case")
    add_edit_flag_page.select_colour("orange")
    add_edit_flag_page.enter_label("Easy to Find")
    add_edit_flag_page.enter_priority(0)
    add_edit_flag_page.enter_blocking_approval(blocks_finalising)

    Shared(driver).click_submit()


@when("I edit the flag I just made")
def edit_existing_flag(driver, context):
    flags_list_page = FlagsListPage(driver)
    add_edit_flag_page = AddEditFlagPage(driver)
    flags_list_page.click_edit_link()

    context.flag_name = f"Edited flag {utils.get_formatted_date_time_d_h_m_s()}"
    add_edit_flag_page.enter_name(context.flag_name)
    add_edit_flag_page.select_colour("red")
    add_edit_flag_page.enter_label("Hard to Find")
    add_edit_flag_page.enter_priority(1)

    Shared(driver).click_submit()


@then("I see the flag in the flag list")
def i_see_flag_in_list(driver, context):
    Shared(driver).filter_by_name(context.flag_name)
    assert context.flag_name in Shared(driver).get_text_of_table()


@when("I deactivate the flag")
def deactivate_flag(driver, context):
    FlagsListPage(driver).click_deactivate_link()
    functions.click_submit(driver, "Deactivated")


@when("I click only show deactivated")
def only_show_deactivated_flags(driver, context):
    FlagsListPage(driver).click_only_show_deactivated()


@when("I reactivate the flag")
def reactivate_flag(driver, context):
    FlagsListPage(driver).click_reactivate_link()
    functions.click_submit(driver, "Active")


@then("I cannot finalise the case due to the blocking flag")
def cannot_finalise_blocking_flag(driver, context):
    final_advice = FinalAdvicePage(driver)
    assert not final_advice.can_finalise()
    assert context.flag_name in final_advice.get_blocking_flags_text()


@when("I go to flags")  # noqa
def go_to_flags(driver, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/flags/")


@when("I select a previously created flag")  # noqa
def assign_flags_to_case(driver, context):  # noqa
    CaseFlagsPages(driver).select_flag(context.flag_name)
    functions.click_submit(driver)


@then("The previously created flag is assigned to the case")  # noqa
def assert_flag_is_assigned(driver, context):  # noqa
    assert CasePage(driver).is_flag_in_applied_flags_list(context.flag_name), (
        "Flag " + context.flag_name + " is not applied to the case"
    )
