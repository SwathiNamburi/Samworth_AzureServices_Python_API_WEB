import allure
import pytest

from classes.api_commons.api_calls import APICalls
from classes.mq_commons.abs.asb_helper import AzureServiceBusHelper
from classes.web_commons.anypoint_platform.anypoint_homepage import AnypointHomePage
from classes.web_commons.anypoint_platform.runtime_manager_page import RuntimeManager
from classes.web_commons.azure_service_bus.asb_homepage import ASBHomePage
from classes.web_commons.azure_service_bus.service_bus_explorer_page import ServiceBusExplorer
from utilities.allure_report import AllureReport
from utilities.browser_manager import BrowserManager
from utilities.config_reader import ConfigReader

@pytest.mark.smoke
@allure.feature("Post Events")
@allure.story("Valid Update Event")
@allure.severity(allure.severity_level.NORMAL)
def test_update_event(driver):

    response_event_id = None
    api = APICalls()

    runtime_manager_page = RuntimeManager(driver)
    asb_connection_string = ConfigReader.get_api_config("ASB_CONNECTION_STRING")

    # Generate unique event ID using API call
    response_body, input_event_id = api.create_event_api_call("update_event.json")
    response_status = response_body["data"]["status"]
    assert "Accepted" in response_status

    response_event_id = response_body["id"]
    print(f"Created Event ID: {response_event_id}")
    print(f"Input Event ID: {input_event_id}")

    # ========================================================
    # SWITCH TO ANYPOINT TAB
    # ========================================================

    driver.switch_to.window(
        driver.anypoint_tab
    )

    # Select Runtime Manager and verify event ID in logs
    runtime_manager_page.goto_runtime_verify_post_logs_matched(response_status,response_event_id)# Select Runtime Manager

    # Create ASB helper object
    asb_helper = AzureServiceBusHelper(asb_connection_string)

    # Expected ID
    expected_event_id = response_event_id

    #Fetch latest message ID from topic
    actual_message_id = asb_helper.get_last_message_id(
        "com.sb.rp.npd.topic",
        "com.sb.rp.npd.subs"
    )

    print("Actual Message ID:", actual_message_id)

    # Assertion
    assert actual_message_id == expected_event_id
    AllureReport.attach_text(expected_event_id,"ASB Topic Message ID matched with Create Event Response Event ID")


