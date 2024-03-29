import os
from pytest_bdd import when, scenarios, then, parsers
import xml.etree.ElementTree as ET

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ui_tests.caseworker.pages.application_page import ApplicationPage
from ui_tests.caseworker.pages.case_list_page import CaseListPage
from ui_tests.caseworker.pages.shared import Shared


scenarios("../features/enforcement.feature", strict_gherkin=False)


@when("I click export enforcement xml")
def export_enforcement_xml(driver):
    CaseListPage(driver).click_export_enforcement_xml()


@then("the enforcement check is audited")
def enforcement_audit(driver, internal_url, context):
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)
    assert "exported the case for enforcement check" in Shared(driver).get_audit_trail_text()


@then(parsers.parse('the file "{filename}" is downloaded'))
def enforcement_file_download_check(filename):
    assert filename in os.listdir("/tmp")


@then(parsers.parse('the downloaded file should include "{party_type}" "{tag}" as "{value}"'))
def enforcement_file_content_check(party_type, tag, value):
    tree = ET.parse("/tmp/enforcement_check.xml")
    root = tree.getroot()

    # get values of all party_types as the file can contain multiple entries
    nodes = root.findall(f".//STAKEHOLDER[SH_TYPE='{party_type}']")
    party_values = set([child.text for node in nodes for child in node.getchildren() if child.tag == tag])
    assert value in party_values


@when(parsers.parse('I include "{party_type}" details to generate import file'))
def generate_enforcement_check_import_file(party_type):
    tree = ET.parse("/tmp/enforcement_check.xml")
    root = tree.getroot()

    # get values of all party_types as the file can contain multiple entries
    nodes = root.findall(f".//STAKEHOLDER[SH_TYPE='{party_type}']")
    assert len(nodes) >= 1
    code1_list = []
    code2_list = []
    for node in nodes:
        for item in list(node):
            if item.tag == "ELA_ID":
                code1_list.append(item.text)
            if item.tag == "SH_ID":
                code2_list.append(item.text)

    assert len(code1_list) > 0
    assert len(code2_list) > 0
    assert len(code1_list) == len(code2_list)
    import_xml_string = '<?xml version="1.0" ?>\n<SPIRE_UPLOAD_FILE>\n'
    for code1, code2 in zip(code1_list, code2_list):
        import_xml_string += (
            f"<SPIRE_RETURNS><CODE1>{code1}</CODE1><CODE2>{code2}</CODE2><FLAG>N</FLAG></SPIRE_RETURNS>\n"
        )

    import_xml_string += "</SPIRE_UPLOAD_FILE>\n"

    with open("/tmp/enforcement_check_import.xml", "w") as f:
        f.write(import_xml_string)


@when("I import the generated enforcement check xml file")
def i_import_generated_enforcement_check_xml_file(driver):  # noqa
    driver.find_element_by_id("button-import-xml").click()
    file_input = driver.find_element_by_name("file")
    file_input.clear()
    file_input.send_keys("/tmp/enforcement_check_import.xml")
    upload_btn = driver.find_element_by_class_name("govuk-button")
    upload_btn.click()

    banner = driver.find_element_by_class_name("app-snackbar__content")
    assert "Enforcement XML imported successfully" in banner.text

    driver.find_element_by_link_text("Back to queue").click()


@then(parsers.parse('the application is removed from "{queue}" queue'))
def application_removed_from_queue(driver, queue):
    ASSIGNED_QUEUES_ID = "assigned-queues"
    WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_element_located((By.ID, ASSIGNED_QUEUES_ID))
    ).is_enabled()
    queue_list = driver.find_element_by_id(ASSIGNED_QUEUES_ID).text.split("\n")
    assert queue not in queue_list


@then("I cleanup the temporary files created")
def application_removed_from_queue():
    download_dir = "/tmp"
    for file in [f for f in os.listdir(download_dir) if f.endswith(".xml")]:
        try:
            os.remove(f"{download_dir}/{file}")
        except OSError:
            pass
