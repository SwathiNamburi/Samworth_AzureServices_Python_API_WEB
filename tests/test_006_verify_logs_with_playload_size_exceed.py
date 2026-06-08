import allure
import pytest

from classes.api_commons.api_calls import APICalls
from classes.web_commons.anypoint_platform.anypoint_homepage import AnypointHomePage
from classes.web_commons.anypoint_platform.runtime_manager_page import RuntimeManager
from classes.web_commons.azure_service_bus.asb_homepage import ASBHomePage
from classes.web_commons.azure_service_bus.service_bus_explorer_page import ServiceBusExplorer
from classes.web_commons.freshservice_portal.fresh_service_homepage import FreshServiceHomepage
from classes.web_commons.freshservice_portal.fresh_service_incident_management_page import FreshServiceIncidentPage
from utilities.browser_manager import BrowserManager
from utilities.config_reader import ConfigReader

@pytest.mark.smoke
@allure.feature("Post Events")
@allure.story("Playload Size Exceed")
@allure.severity(allure.severity_level.CRITICAL)

def test_post_event_with_playload_size_exceed(driver):

    api = APICalls()

    runtime_manager_page = RuntimeManager(driver)
    fresh_service_incident_page = FreshServiceIncidentPage(driver)

    # Generate unique event ID using API call
    response_body, input_event_id = api.create_event_api_call("payload_size_exceed.json")
    response_status = response_body["status"]
    assert response_status in ["400", "404"]  # Expecting an error status code due to invalid tenant ID

    response_title = response_body["title"]
    response_instance_id = response_body["instance"]
    response_detail = response_body["detail"]

    # Extract only first error line
    expected_alert_msg = response_detail.split("\n")[0]
    print(expected_alert_msg)

    print(f" input event id: {input_event_id}")
    print(f"instance id: {response_instance_id}")
    print(f"title: {response_title}")
    print(f"detail: {response_detail}")

    # ========================================================
    # SWITCH TO ANYPOINT TAB
    # ========================================================
    driver.switch_to.window(
        driver.anypoint_tab
    )
    # Select Runtime Manager and verify event ID in logs
    runtime_manager_page.goto_runtime_verify_logs_instance_id_matched(
                response_status,response_instance_id,"Bad request")  # Select Runtime Manager

    # ========================================================
    # SWITCH TO Fresh Service TAB
    # ========================================================
    driver.switch_to.window(
        driver.freshservice_tab
    )

    #Verify incident in Fresh Service
    fresh_service_incident_page.search_and_capture_incident(response_instance_id,expected_alert_msg)

