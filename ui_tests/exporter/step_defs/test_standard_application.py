from pytest_bdd import scenarios, when, then, parsers, given

from ui_tests.exporter.pages.end_use_details_form_page import EndUseDetailsFormPage
from ui_tests.exporter.conftest import (
    enter_type_of_application,
    enter_application_name,
    enter_permanent_or_temporary,
    enter_export_licence,
    enter_case_note_text,
    click_post_note,
    answer_firearms_question,
)
from ui_tests.exporter.pages.add_new_external_location_form_page import AddNewExternalLocationFormPage
from ui_tests.exporter.pages.add_goods_details import AddGoodDetails
from ui_tests.exporter.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_tests.exporter.pages.exporter_hub_page import ExporterHubPage
from ui_tests.exporter.pages.location_type_page import LocationTypeFormPage
from ui_tests.exporter.pages.submitted_applications_page import SubmittedApplicationsPages
from ui_tests.exporter.pages.which_location_form_page import WhichLocationFormPage
from ui_tests.exporter.pages.add_end_user_pages import AddEndUserPages
from ui_tests.exporter.pages.attach_document_page import AttachDocumentPage
from ui_tests.exporter.pages.external_locations_page import ExternalLocationsPage
from ui_tests.exporter.pages.generic_application.ultimate_end_users import GenericApplicationUltimateEndUsers
from ui_tests.exporter.pages.preexisting_locations_page import PreexistingLocationsPage
from ui_tests.exporter.pages.shared import Shared
from ui_tests.exporter.pages.standard_application.good_details import StandardApplicationGoodDetails
from ui_tests.exporter.pages.standard_application.goods import StandardApplicationGoodsPage
from tests_common import functions

from ui_tests.exporter.pages.generic_application.task_list import TaskListPage

from faker import Faker

fake = Faker()

scenarios(
    "../features/goods.feature",
    "../features/submit_standard_application.feature",
    "../features/edit_standard_application.feature",
    "../features/siel_firearm_application.feature",
    strict_gherkin=False,
)


@when("I click on the add button")
def i_click_on_the_add_button(driver):
    GenericApplicationUltimateEndUsers(driver).click_add_ultimate_recipient_button()


@when("I remove an ultimate end user so there is one less")
def i_remove_an_ultimate_end_user(driver):
    no_of_ultimate_end_users = Shared(driver).get_size_of_table_rows()
    driver.find_element_by_link_text("Remove").click()
    total = no_of_ultimate_end_users - Shared(driver).get_size_of_table_rows()
    assert total == 1, "total on the ultimate end users summary is incorrect after removing ultimate end user"


@then("there is only one ultimate end user")
def one_ultimate_end_user(driver):
    assert (
        len(GenericApplicationUltimateEndUsers(driver).get_ultimate_recipients()) == 1
    ), "total on the application overview is incorrect after removing ultimate end user"
    functions.click_back_link(driver)


@then(parsers.parse('"{button}" link is present'))
def download_and_delete_is_links_are_present(driver, button):
    shared = Shared(driver)
    latest_ueu_links = [link.text for link in shared.get_links_of_table_row(-1)]
    assert button in latest_ueu_links


@when(  # noqa
    parsers.parse('I select the location at position "{position_number}" in external locations list and continue')
)
def assert_checkbox_at_position(driver, position_number):  # noqa
    preexisting_locations_page = PreexistingLocationsPage(driver)
    preexisting_locations_page.click_external_locations_checkbox(int(position_number) - 1)
    functions.click_submit(driver)


@then(parsers.parse('I see "{number_of_locations}" locations'))  # noqa
def i_see_a_number_of_locations(driver, number_of_locations):  # noqa
    assert len(driver.find_elements_by_css_selector("tbody tr")) == int(number_of_locations)


@when("I click on add new address")  # noqa
def i_click_on_add_new_address(driver):  # noqa
    external_locations_page = ExternalLocationsPage(driver)
    external_locations_page.click_add_new_address()


@when("I click on preexisting locations")  # noqa
def i_click_add_preexisting_locations(driver):  # noqa
    external_locations_page = ExternalLocationsPage(driver)
    external_locations_page.click_preexisting_locations()


@when("I add an incorporated good to the application")  # noqa
def i_add_a_non_incorporated_good_to_the_application(driver, context):  # noqa
    StandardApplicationGoodsPage(driver).click_add_preexisting_good_button()

    # Click the "Add to application" link on the first good
    driver.find_elements_by_id("add-to-application")[0].click()

    # Enter good details
    StandardApplicationGoodDetails(driver).enter_value("1")
    StandardApplicationGoodDetails(driver).enter_quantity("2")
    StandardApplicationGoodDetails(driver).select_unit("Number of articles")
    StandardApplicationGoodDetails(driver).check_is_good_incorporated_true()
    context.is_good_incorporated = "Yes"

    functions.click_submit(driver)


@when("I choose to add a new product")  # noqa
def i_choose_to_add_a_new_product(driver, context):  # noqa
    StandardApplicationGoodsPage(driver).click_add_new_good_button()


@when("I choose to add a product from product list")  # noqa
def i_choose_to_add_product_from_product_list(driver, context):  # noqa
    StandardApplicationGoodsPage(driver).click_add_preexisting_good_button()


@when(parsers.parse('I choose to review the product details of product "{index:d}"'))  # noqa
def i_choose_to_review_product_details(driver, index):  # noqa
    # Click the "View" link on the given good index
    detail_link = driver.find_element_by_id("import-product-view-product")
    detail_link.click()


@when("I see option to add product to application on details page")
def i_see_option_to_add_product_to_application(driver):
    add_to_application_btn = driver.find_element_by_id("button-add-good-to-application")


@when(parsers.parse('I append "{text}" to description and submit'))  # noqa
def i_update_description(driver, text):  # noqa
    change_description = driver.find_elements_by_id("link-edit-description")[0]
    change_description.click()

    desc_element = driver.find_element_by_id("description")
    updated_description = f"{desc_element.text} {text}"
    desc_element.clear()
    desc_element.send_keys(updated_description)

    functions.click_submit(driver)


@when("I add product to application")
def i_add_product_to_application(driver, context):
    add_to_application_btn = driver.find_element_by_id("button-add-good-to-application")
    add_to_application_btn.click()

    # Enter good details
    StandardApplicationGoodDetails(driver).enter_value("1")
    StandardApplicationGoodDetails(driver).enter_quantity("2")
    StandardApplicationGoodDetails(driver).select_unit("Number of articles")
    StandardApplicationGoodDetails(driver).check_is_good_incorporated_true()
    context.is_good_incorporated = "Yes"

    functions.click_submit(driver)


@given("I seed an end user for the draft")
def seed_end_user(add_end_user_to_application):
    pass


@when("I select that I want to copy an existing party")
def copy_existing_party_yes(driver):
    AddEndUserPages(driver).create_new_or_copy_existing(copy_existing=True)


@then("I can select the existing party in the table")
def party_table(driver, context):
    text = [context.end_user[key] for key in ["name", "address"]]
    text.append(context.end_user["country"]["name"])
    row = Shared(driver).get_table_row(1)

    for string in text:
        assert string in row.text


@when("I click copy party")
def copy_party(driver):
    AddEndUserPages(driver).click_copy_existing_button()


@then("I see the party name is already filled in")
def party_name_autofill(driver, context):
    assert AddEndUserPages(driver).get_name() == context.end_user["name"]


@then("I see the party website is already filled in")
def party_website_autofill(driver, context):
    assert AddEndUserPages(driver).get_website() == context.end_user["website"]


@then("I see the party address and country is already filled in")
def party_address_autofill(driver, context):
    assert AddEndUserPages(driver).get_address() == context.end_user["address"]
    assert AddEndUserPages(driver).get_country() == context.end_user["country"]["name"]


@when("I skip uploading a document")
def skip_document_upload(driver, context):
    AttachDocumentPage(driver).click_save_and_return_to_overview_link()
    # Setup for checking on overview page
    context.type_end_user = context.end_user["sub_type"]["value"]
    context.name_end_user = context.end_user["name"]
    context.address_end_user = context.end_user["address"]


@when("I filter for my previously created end user")
def filter_for_party(driver, context):
    parties_page = AddEndUserPages(driver)
    parties_page.open_parties_filter()
    parties_page.filter_name(context.end_user["name"])
    parties_page.filter_address(context.end_user["address"])
    parties_page.filter_country(context.end_user["country"]["name"])
    parties_page.submit_filter()


@given("I create a draft")  # noqa
def create_a_draft(add_a_draft):  # noqa
    pass


@when(parsers.parse('I create a standard application of a "{export_type}" export type'))  # noqa
def create_standard_application(driver, export_type, context):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    ApplyForALicencePage(driver).select_licence_type("export_licence")
    functions.click_submit(driver)
    enter_type_of_application(driver, "siel", context)
    enter_permanent_or_temporary(driver, export_type, context)
    enter_application_name(driver, context)
    enter_export_licence(driver, "yes", "123456", context)


@then("I see the application overview")  # noqa
def i_see_the_application_overview(driver, context):  # noqa
    element = TaskListPage(driver).get_text_of_lite_task_list_items()
    assert context.app_name in element

    app_id = driver.current_url.split("/")[-3]
    context.app_id = app_id


@when(parsers.parse('I am on the application overview page entitled "{title}"'))  # noqa
def i_am_on_application_overview_with_title(driver, title):  # noqa
    heading = driver.find_element_by_xpath("//h1").text
    assert heading == title


@then(parsers.parse('I should be taken to the application overview page entitled "{title}"'))  # noqa
def taken_to_application_overview_page(driver, title):
    i_am_on_application_overview_with_title(driver, title)


@when("I delete the application")  # noqa
def i_delete_the_application(driver):  # noqa
    apply = ApplyForALicencePage(driver)
    apply.click_delete_application()
    assert "Applications - LITE" in driver.title, (
        "failed to go to Applications list page after deleting application " "from application overview page"
    )


@when("I add a note to the draft application")  # noqa
def add_a_note_to_draft_application(driver, context):  # noqa
    enter_case_note_text(driver, context)
    click_post_note(driver)
    SubmittedApplicationsPages(driver).assert_case_notes_exists([context.text])

    functions.click_back_link(driver)


@when(parsers.parse('I select "{choice}" for whether or not I want a new or existing location to be added'))  # noqa
def choose_location_type(driver, choice):  # noqa
    which_location_form = WhichLocationFormPage(driver)
    which_location_form.click_on_choice_radio_button(choice)
    functions.click_submit(driver)


@when(parsers.parse('I select a location type of "{location_type}"'))  # noqa
def choose_location_type(driver, location_type):  # noqa
    LocationTypeFormPage(driver).click_on_location_type_radiobutton(location_type)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I fill in new external location form with name: "{name}", address: "{address}" and country: "{country}" and continue'
    )
)
def add_new_external_location(driver, name, address, country):  # noqa
    add_new_external_location_form_page = AddNewExternalLocationFormPage(driver)
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    add_new_external_location_form_page.enter_external_location_country(country)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I fill in new external location form with name: "{name}", address: "{address}" and no country and continue'
    )
)
def add_new_external_location_without_country(driver, name, address):  # noqa
    add_new_external_location_form_page = AddNewExternalLocationFormPage(driver)
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    functions.click_submit(driver)


@when("I create a standard individual transhipment application")  # noqa
def create_standard_individual_transhipment_application(driver, context):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    ApplyForALicencePage(driver).select_licence_type("transhipment")
    functions.click_submit(driver)
    enter_type_of_application(driver, "sitl", context)
    enter_application_name(driver, context)
    enter_export_licence(driver, "yes", "123456", context)


@when("I create a standard individual trade control draft application")  # noqa
def create_standard_individual_trade_control_application(driver, context):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    apply_for_licence_page = ApplyForALicencePage(driver)
    apply_for_licence_page.select_licence_type("trade_control_licence")
    functions.click_submit(driver)
    enter_type_of_application(driver, "sicl", context)
    enter_application_name(driver, context)
    apply_for_licence_page.select_trade_control_activity()
    apply_for_licence_page.select_trade_control_product_category()


@when("I change my reference number")
def change_ref_num(driver, context):  # noqa
    enter_export_licence(driver, "yes", "12345678", context)


@then("I see my edited reference number")
def assert_ref_num(driver):  # noqa
    assert "12345678" in driver.find_element_by_css_selector(".lite-task-list").text


@when(parsers.parse('I answer "{choice}" for compliance with the terms of export from the EU'))  # noqa
def eu_compliant_limitations_end_use_details(driver, choice):  # noqa
    end_use_details = EndUseDetailsFormPage(driver)
    if choice == "Yes":
        end_use_details.answer_is_compliant_limitations_eu(True)
    else:
        end_use_details.answer_is_compliant_limitations_eu(False, fake.sentence(nb_words=30))
    functions.click_submit(driver)


@when(parsers.parse('I answer "{choice}" for products received under transfer licence from the EU'))  # noqa
def eu_military_end_use_details(driver, choice):  # noqa
    end_use_details = EndUseDetailsFormPage(driver)
    if choice == "Yes":
        end_use_details.answer_is_eu_military(True)
    else:
        end_use_details.answer_is_eu_military(False)
    functions.click_submit(driver)


@when(parsers.parse('I select "{choice}" to document available question'))
def check_product_document_available(driver, choice):
    good_details_page = AddGoodDetails(driver)
    good_details_page.set_product_document_availability(choice)
    functions.click_submit(driver)


@when(parsers.parse('I select "{choice}" to document is above official sensitive question'))
def check_product_document_available(driver, choice):
    good_details_page = AddGoodDetails(driver)
    good_details_page.set_product_document_sensitive(choice)
    functions.click_submit(driver)


@when(parsers.parse('I select "{choice}" to registered firearms dealer question'))
def check_product_document_available(driver, choice):
    good_details_page = AddGoodDetails(driver)
    good_details_page.set_registered_firearms_dealer(choice)
    functions.click_submit(driver)
