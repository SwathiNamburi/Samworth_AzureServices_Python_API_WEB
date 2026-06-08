import allure
import pytest

from classes.api_commons.api_calls import APICalls
from classes.mq_commons.abs.asb_helper import AzureServiceBusHelper
from classes.web_commons.anypoint_platform.anypoint_homepage import AnypointHomePage
from classes.web_commons.anypoint_platform.runtime_manager_page import RuntimeManager
from classes.web_commons.azure_service_bus.asb_homepage import ASBHomePage
from classes.web_commons.azure_service_bus.service_bus_explorer_page import ServiceBusExplorer
from classes.web_commons.freshservice_portal.fresh_service_homepage import FreshServiceHomepage
from classes.web_commons.freshservice_portal.fresh_service_incident_management_page import FreshServiceIncidentPage
from utilities.allure_report import AllureReport
from utilities.config_reader import ConfigReader

@pytest.mark.smoke
@allure.feature("Post Events")
@allure.story("ASB Unavailable")
@allure.severity(allure.severity_level.CRITICAL)
def test_ASB_unavailable_with_incorrect_settings(driver):

    api = APICalls()
    runtime_manager_page = RuntimeManager(driver)
    fresh_service_incident_page = FreshServiceIncidentPage(driver)

    # Generate unique event ID using API call
    response_body, input_event_id = api.create_event_api_call("create_event.json")
    response_status = response_body["status"]
    response_instance_id = response_body["instance"]

    assert response_status == "403", f"Expected status code 403, but got {response_status}"

    print(f"response_status: {response_status}")
    print(f"instance id: {response_instance_id}")

    # ========================================================
    # SWITCH TO ANYPOINT TAB
    # ========================================================
    driver.switch_to.window(
        driver.anypoint_tab
    )

    # Select Runtime Manager and verify event ID in logs
    runtime_manager_page.goto_runtime_verify_logs_instance_id_matched_Alert_message(response_status, response_instance_id)  # Select Runtime Manager

    # ========================================================
    # SWITCH TO Fresh Service TAB
    # ========================================================
    driver.switch_to.window(
        driver.freshservice_tab
    )

    fresh_service_incident_page.search_and_capture_incident(input_event_id, "MuleSoft Technical Error")
