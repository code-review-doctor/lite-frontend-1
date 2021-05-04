import requests
from bs4 import BeautifulSoup
from django.template.loader import render_to_string

from caseworker.cases.objects import Case


team1 = {"id": "136cbb1f-390b-4f78-bfca-86300edec300", "name": "team1", "part_of_ecju": None}
team2 = {"id": "47762273-5655-4ce3-afa1-b34112f3e781", "name": "team2", "part_of_ecju": None}

john_smith = {
    "email": "john.smith@example.com",
    "first_name": "John",
    "id": "63c74ddd-c119-48cc-8696-d196218ca583",
    "last_name": "Smith",
    "role_name": "Super User",
    "status": "Active",
    "team": team1,
}
john_doe = {
    "email": "john.doe@example.com",
    "first_name": "John",
    "id": "63c74ddd-c119-48cc-8696-d196218ca583",
    "last_name": "Doe",
    "role_name": "Super User",
    "status": "Active",
    "team": team1,
}
jane_doe = {
    "email": "jane.doe@example.com",
    "first_name": "Jane",
    "id": "24afb1dc-fa1e-40d1-a716-840585c85ebc",
    "last_name": "Doe",
    "role_name": "Super User",
    "status": "Active",
    "team": team2,
}
jane_smith = {
    "email": "jane.smith@example.com",
    "first_name": "Jane",
    "id": "24afb1dc-fa1e-40d1-a716-840585c85ebc",
    "last_name": "Smith",
    "role_name": "Super User",
    "status": "Active",
    "team": team2,
}
dummy_advice = {
    "id": "f4f3476f-9849-49d1-973e-62b185085a64",
    "text": "",
    "note": "",
    "type": {"key": "approve", "value": "Approve"},
    "level": "user",
    "proviso": None,
    "denial_reasons": [],
    "footnote": None,
    "user": jane_smith,
    "created_at": "2021-03-18T11:27:56.625251Z",
    "good": None,
    "goods_type": None,
    "country": None,
    "end_user": "633178cd-83ec-4773-8829-c19065912565",
    "ultimate_end_user": None,
    "consignee": None,
    "third_party": None,
}


def test_advice_section_no_user_advice_checkboxes_visible_no_combine_button(data_standard_case):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    context["current_user"] = jane_doe
    context["current_advice_level"] = ["user"]
    html = render_to_string("case/tabs/user-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" in soup.find(id="button-combine-user-advice").parent["class"]
    assert soup.find(id="link-select-all-goods")
    assert soup.find(id="link-select-all-destinations")


def test_advice_section_no_user_advice_checkboxes_visible_no_combine_button_grouped_view(
    data_standard_case, rf, client
):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    context["current_user"] = jane_doe
    context["current_advice_level"] = ["user"]
    case_id = context["case"]["id"]
    queue_id = context["queue"]["id"]

    request = rf.get(f"/queues/{queue_id}/cases/{case_id}/user-advice/?grouped-advice-view=True")
    request.session = client.session
    request.requests_session = requests.Session()

    html = render_to_string("case/tabs/user-advice.html", context=context, request=request)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" in soup.find(id="button-combine-user-advice").parent["class"]
    assert soup.find(id="button-select-all-no_advice")


def test_advice_section_user_can_combine_advice_from_own_team(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    context["case"].advice = [dummy_advice]
    context["current_user"] = jane_doe
    context["current_advice_level"] = ["user"]

    html = render_to_string("case/tabs/user-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" not in soup.find(id="button-combine-user-advice").parent["class"]


def test_advice_section_user_cannot_combine_advice_from_other_team(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    advice_1 = {**dummy_advice}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    context["case"].advice = [advice_1]
    context["current_user"] = john_smith
    context["current_advice_level"] = ["user"]

    html = render_to_string("case/tabs/user-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" in soup.find(id="button-combine-user-advice").parent["class"]


def test_advice_section_user_can_clear_advice_from_own_team(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    team_advice = {**dummy_advice}
    team_advice["level"] = "team"
    context["case"].advice = [team_advice]
    context["current_user"] = jane_doe
    context["current_advice_level"] = ["user", "team"]

    html = render_to_string("case/tabs/team-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" not in soup.find(id="button-clear-team-advice").parent["class"]


def test_advice_section_user_cannot_clear_advice_from_other_team(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    team_advice = {**dummy_advice}
    team_advice["level"] = "team"
    context["case"].advice = [team_advice]
    context["current_user"] = john_smith
    context["current_advice_level"] = ["user", "team"]

    html = render_to_string("case/tabs/team-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" in soup.find(id="button-clear-team-advice").parent["class"]


def test_advice_section_user_cannot_clear_if_no_team_advice(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    advice = {**dummy_advice}
    advice["level"] = "user"
    context["case"].advice = [advice]
    context["current_user"] = john_doe
    context["current_advice_level"] = ["user"]

    html = render_to_string("case/tabs/team-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert not soup.find(id="button-clear-team-advice")


def test_advice_section_user_can_combine_team_advice_from_own_team(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    team_advice = {**dummy_advice}
    team_advice["level"] = "team"
    context["case"].advice = [team_advice]
    context["current_user"] = jane_doe
    context["current_advice_level"] = ["user", "team"]

    html = render_to_string("case/tabs/team-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" not in soup.find(id="button-combine-team-advice").parent["class"]


def test_advice_section_user_cannot_combine_team_advice_if_no_advice_from_own_team(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    team_advice = {**dummy_advice}
    team_advice["level"] = "team"
    context["case"].advice = [team_advice]
    context["current_user"] = john_smith
    context["current_advice_level"] = ["user", "team"]

    html = render_to_string("case/tabs/team-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" in soup.find(id="button-combine-team-advice").parent["class"]


def test_advice_section_user_can_clear_final_advice_from_own_team(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    advice = {**dummy_advice}
    advice["level"] = "final"
    context["case"].advice = [advice]
    context["current_user"] = jane_doe
    context["current_advice_level"] = ["user", "team", "final"]

    html = render_to_string("case/tabs/final-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert soup.find(id="button-clear-final-advice")


def test_advice_section_user_cannot_clear_final_advice_from_other_team(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    advice = {**dummy_advice}
    advice["level"] = "final"
    context["case"].advice = [advice]
    context["current_user"] = john_doe
    context["current_advice_level"] = ["user", "team", "final"]

    html = render_to_string("case/tabs/final-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert not soup.find(id="button-clear-final-advice")


def test_advice_section_user_cannot_clear_if_no_final_advice(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    advice = {**dummy_advice}
    advice["level"] = "team"
    context["case"].advice = [advice]
    context["current_user"] = john_doe
    context["current_advice_level"] = ["user", "team"]

    html = render_to_string("case/tabs/final-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert not soup.find(id="button-clear-final-advice")


def test_advice_section_user_cannot_finalise(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    advice = {**dummy_advice}
    advice["level"] = "final"
    context["case"].advice = [advice]
    context["current_user"] = john_doe
    context["current_advice_level"] = ["user", "team", "final"]
    context["can_finalise"] = False

    html = render_to_string("case/tabs/final-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" in soup.find(id="button-finalise").parent["class"]


def test_advice_section_user_can_finalise(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    advice = {**dummy_advice}
    advice["level"] = "final"
    context["case"].advice = [advice]
    context["current_user"] = john_doe
    context["current_advice_level"] = ["user", "team", "final"]
    context["can_finalise"] = True

    html = render_to_string("case/tabs/final-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" not in soup.find(id="button-finalise").parent["class"]