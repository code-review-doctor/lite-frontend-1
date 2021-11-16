import os
from collections import OrderedDict

import tests_common.tools.helpers as utils


STEP_THROUGH = False  # Gives a prompt for every step in the terminal
SCENARIO_HISTORY = OrderedDict()
SCENARIO_DIVIDER_LEN = 70


def print_scenario_history(entry):
    scenario = entry["scenario"]
    steps = entry["steps"]
    print("*******************************************\n")
    print(f"SCENARIO: {scenario.feature.description}\n")
    for step in steps:
        print(f"\t{step.keyword.upper()} {step.name}")
    print("\n*******************************************")


def print_scenario_history_last_entry():
    print_scenario_history(list(SCENARIO_HISTORY.values())[-1])


def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    """
    Runs before each step
    """
    if scenario not in SCENARIO_HISTORY:
        print()
        print("*"*SCENARIO_DIVIDER_LEN)
        print()
        print(f"SCENARIO: {scenario.feature.description}")
    print(f"\t {step.keyword.upper()} {step.name}")

    try:
        SCENARIO_HISTORY[scenario]["steps"].append(step)
    except KeyError:
        SCENARIO_HISTORY[scenario] = {
            "steps": [step],
            "scenario": scenario,
        }

    if STEP_THROUGH:
        import IPython

        IPython.embed(using=False)


def pytest_configure(config):
    if config.option.step_through:
        global STEP_THROUGH  # pylint: disable=global-statement
        STEP_THROUGH = config.option.step_through


def pytest_addoption(parser):
    env = str(os.environ.get("ENVIRONMENT"))
    if env == "None":
        env = "dev"
    parser.addoption("--headless", action="store_true", default=False)
    parser.addoption(
        "--step-through", action="store_true", default=STEP_THROUGH, help="Allow stepping through each scenario step"
    )
    if env == "local":
        parser.addoption(
            "--exporter_url", action="store", default=f"http://localhost:{str(os.environ.get('PORT'))}/", help="url"
        )
        parser.addoption(
            "--internal_url", action="store", default="http://localhost:" + str(os.environ.get("PORT")), help="url"
        )
        lite_api_url = os.environ.get("LOCAL_LITE_API_URL", os.environ.get("LITE_API_URL"),)
        parser.addoption(
            "--lite_api_url", action="store", default=lite_api_url, help="url",
        )
    else:
        parser.addoption(
            "--exporter_url",
            action="store",
            default=f"https://exporter.lite.service.{env}.uktrade.digital/",
            help="url",
        )
        parser.addoption(
            "--internal_url",
            action="store",
            default="https://internal.lite.service." + env + ".uktrade.digital/",
            help="url",
        )
        parser.addoption(
            "--lite_api_url", action="store", default=f"https://lite-api-{env}.london.cloudapps.digital/", help="url",
        )
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")


def pytest_exception_interact(node, report):
    if node and report.failed and hasattr(node, "funcargs"):
        driver = node.funcargs.get("driver")
        if driver:
            utils.save_screenshot(driver=driver, name=node.name)
