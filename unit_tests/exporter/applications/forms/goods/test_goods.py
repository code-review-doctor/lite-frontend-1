from copy import deepcopy
from uuid import UUID

import pytest
import requests

from exporter.applications.forms import goods


application_id = UUID("2a199722-75fc-4699-abfc-ddfb30381c0f")
sub_case_type_siel = {"key": "standard", "value": "Standard Licence"}


@pytest.fixture(scope="session")
def good_template():
    return {
        "component_details": None,
        "control_list_entries": [],
        "id": "7aa98481-c547-448c-9fd3-1d22d0eb7c33",
        "information_security_details": None,
        "is_component": None,
        "is_good_controlled": {"key": "False", "value": "No"},
        "is_military_use": None,
        "is_pv_graded": {"key": "no", "value": "No"},
        "modified_military_use_details": None,
        "part_number": "",
        "pv_grading_details": None,
        "software_or_technology_details": None,
        "uses_information_security": None,
        # to be set by fixture
        "item_category": {},
        "name": "good",
        "description": "",
        "firearm_details": {},
    }


@pytest.fixture(scope="session")
def good_ammo(good_template):
    return {
        **good_template,
        "name": "Ammunition",
        "description": "box of 25 game shot cartridges",
        "item_category": {"key": "group2_firearms", "value": "Firearms"},
        "firearm_details": {
            "calibre": "16 gramme",
            "has_identification_markings": False,
            "has_proof_mark": None,
            "identification_markings_details": None,
            "is_covered_by_firearm_act_section_one_two_or_five": False,
            "no_identification_markings_details": "it's ammo",
            "no_proof_mark_details": "",
            "section_certificate_date_of_expiry": None,
            "section_certificate_number": None,
            "type": {"key": "ammunition", "value": "Ammunition"},
            "year_of_manufacture": 2019,
            "number_of_items": 3,
        },
    }


@pytest.fixture(scope="session")
def good_shotgun(good_template):
    return {
        **good_template,
        "name": "Shotgun",
        "description": "A shotgun",
        "item_category": {"key": "group2_firearms", "value": "Firearms"},
        "firearm_details": {
            "calibre": "12 guage",
            "has_identification_markings": False,
            "has_proof_mark": None,
            "identification_markings_details": None,
            "is_covered_by_firearm_act_section_one_two_or_five": False,
            "no_identification_markings_details": "dd",
            "no_proof_mark_details": "",
            "section_certificate_date_of_expiry": None,
            "section_certificate_number": None,
            "type": {"key": "firearms", "value": "Firearms"},
            "year_of_manufacture": 2020,
            "number_of_items": 3,
        },
    }


@pytest.fixture(scope="session")
def good_gun_barrel(good_template):
    return {
        **good_template,
        "name": "Gun barrel",
        "description": "A barrel",
        "item_category": {"key": "group2_firearms", "value": "Firearms"},
        "firearm_details": {
            "calibre": "12 guage",
            "has_identification_markings": False,
            "has_proof_mark": None,
            "identification_markings_details": None,
            "is_covered_by_firearm_act_section_one_two_or_five": False,
            "no_identification_markings_details": "foo",
            "no_proof_mark_details": "",
            "section_certificate_date_of_expiry": None,
            "section_certificate_number": None,
            "type": {"key": "components_for_firearms", "value": "Components for firearms"},
            "year_of_manufacture": 2020,
            "number_of_items": 3,
        },
    }


@pytest.fixture(scope="session")
def good_widget(good_template):

    return {
        **good_template,
        "name": "Widget",
        "description": "A widget",
        "item_category": {"key": "group1_components", "value": "Components, modules or accessories of something"},
    }


@pytest.fixture
def default_request(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    return request


def test_good_on_application_form_ammunition(default_request, good_ammo, mock_units):
    form = goods.unit_quantity_value(
        request=default_request,
        good=good_ammo,
        sub_case_type=sub_case_type_siel,
        application_id=application_id,
        back_url="/the/url/",
    )

    assert len(form.questions) == 6
    question_titles = [getattr(q, "title", None) for q in form.questions]
    assert goods.firearm_proof_mark_field().title in question_titles
    assert goods.firearm_is_deactivated_field().title in question_titles


def test_good_on_application_form_firearm(default_request, good_shotgun, mock_units):
    form = goods.unit_quantity_value(
        request=default_request,
        good=good_shotgun,
        sub_case_type=sub_case_type_siel,
        application_id=application_id,
        back_url="/the/url/",
    )

    assert len(form.questions) == 6
    question_titles = [getattr(q, "title", None) for q in form.questions]
    assert goods.firearm_proof_mark_field().title in question_titles
    assert goods.firearm_is_deactivated_field().title in question_titles


def test_good_on_application_form_firearm_component(default_request, good_gun_barrel, mock_units):
    form = goods.unit_quantity_value(
        request=default_request,
        good=good_gun_barrel,
        sub_case_type=sub_case_type_siel,
        application_id=application_id,
        back_url="/the/url/",
    )

    assert len(form.questions) == 6
    assert form.questions[-1].options[0].components[0].title == goods.firearm_proof_mark_field().title
    assert form.questions[-2].title == goods.firearm_is_deactivated_field().title


def test_good_on_application_form_not_firearm(default_request, good_widget, mock_units):
    form = goods.unit_quantity_value(
        request=default_request,
        good=good_widget,
        sub_case_type=sub_case_type_siel,
        application_id=application_id,
        back_url="/the/url/",
    )

    assert len(form.questions) == 6
    assert form.questions[-1].title != goods.firearm_proof_mark_field().title


def test_good_on_application_form_group_good_without_number_of_items(default_request, good_ammo):
    application = {}
    good_data = deepcopy(good_ammo)
    del good_data["firearm_details"]["number_of_items"]
    form_group = goods.good_on_application_form_group(
        request=default_request,
        is_preexisting=True,
        good=good_data,
        sub_case_type=sub_case_type_siel,
        draft_pk=None,
        application=application,
        show_attach_rfd=False,
        relevant_firearm_act_section=None,
        is_firearm=False,
        is_firearm_ammunition_or_component=True,
        is_firearms_accessory=False,
        is_firearms_software_or_tech=False,
        back_url="",
        show_serial_numbers_form=True,
        is_rfd=False,
    )

    assert len(form_group.forms) == 6


def test_good_on_application_form_group_user_is_rfd(default_request, good_ammo):
    application = {}
    form_group = goods.good_on_application_form_group(
        request=default_request,
        is_preexisting=True,
        good=good_ammo,
        sub_case_type=sub_case_type_siel,
        draft_pk=None,
        application=application,
        show_attach_rfd=True,
        relevant_firearm_act_section=None,
        is_firearm=False,
        is_firearm_ammunition_or_component=True,
        is_firearms_accessory=False,
        is_firearms_software_or_tech=False,
        back_url="",
        show_serial_numbers_form=True,
        is_rfd=True,
    )

    assert len(form_group.forms) == 7
