import pytest

from copy import deepcopy
from django.urls import reverse

from core import client
from caseworker.advice import services


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(request, data_queue, data_standard_case):
    return reverse(
        f"cases:countersign_review", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_countersign_approve_all_put(
    authorized_client,
    requests_mock,
    data_standard_case,
    standard_case_with_advice,
    advice_for_countersign,
    mock_gov_user,
    url,
):
    countersign_advice_url = f"/cases/{data_standard_case['case']['id']}/countersign-advice/"
    requests_mock.put(client._build_absolute_uri(countersign_advice_url), json={})
    case_data = deepcopy(data_standard_case)
    case_data["case"]["data"]["goods"] = standard_case_with_advice["data"]["goods"]
    case_data["case"]["advice"] = advice_for_countersign

    requests_mock.get(client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}"), json=case_data)
    requests_mock.get(
        client._build_absolute_uri(f"/gov_users/{mock_gov_user['user']['id']}"), json=mock_gov_user,
    )

    user_team_advice = services.filter_advice_by_users_team(advice_for_countersign, mock_gov_user["user"])
    advice_to_countersign = services.filter_advice_by_level(user_team_advice, ["user"])

    data = {
        "form-TOTAL_FORMS": [f"{len(advice_to_countersign)}"],
        "form-INITIAL_FORMS": ["0"],
        "form-MIN_NUM_FORMS": [f"{len(advice_to_countersign)}"],
        "form-MAX_NUM_FORMS": [f"{len(advice_to_countersign)}"],
        "submit": ["Submit"],
    }
    for index, item in enumerate(advice_for_countersign):
        data[f"form-{index}-agree_with_recommendation"] = ["yes"]
        data[f"form-{index}-approval_reasons"] = [f"reason{index + 1}"]

    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    history = requests_mock.request_history
    assert countersign_advice_url in history[5].url
    assert history[5].method == "PUT"
    assert history[5].json() == [
        {
            "id": "b32d7dfa-a90d-4b37-adac-db231d4b83be",
            "countersigned_by": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "countersign_comments": "reason1",
        },
        {
            "id": "c9a96d84-6a6b-421d-bbbb-b12b9577d46e",
            "countersigned_by": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "countersign_comments": "reason2",
        },
    ]