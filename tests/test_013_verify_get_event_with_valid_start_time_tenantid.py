import allure
import pytest

from classes.api_commons.api_calls import APICalls
from classes.db_commons.cosmos_db.cosmos_helper import CosmosDBHelper
from classes.mq_commons.abs.asb_helper import AzureServiceBusHelper
from classes.web_commons.anypoint_platform.anypoint_homepage import AnypointHomePage
from classes.web_commons.anypoint_platform.runtime_manager_page import RuntimeManager
from utilities.allure_report import AllureReport
from utilities.config_reader import ConfigReader

@pytest.mark.smoke
@allure.feature("Get Events")
@allure.story("Valid Start Time and Tenant ID")
@allure.severity(allure.severity_level.NORMAL)
def test_get_evens_with_valid_time_and_tenantid(driver):

    api = APICalls()

    asb_connection_string = ConfigReader.get_api_config("ASB_CONNECTION_STRING")
    asb_helper = AzureServiceBusHelper(asb_connection_string)
    runtime_manager_page = RuntimeManager(driver)

    # ==========================================
    # BUILD PAYLOAD
    # ==========================================
    payload_str, event_id, input_time = api.get_payload("create_event.json")
    print(f"Generated Event ID: {event_id}")
    print(f"Generated Input time: {input_time}")

    asb_helper.send_message_to_topic(payload_str, "com.sb.npd.rp.topic")

    # ==========================================
    # GET EVENTS API CALL
    # ==========================================
    #start_time = input_time
    response, response_body = api.get_events_api_call_with_tenantid(input_time, tenant_id="savourypastry")
    # ==========================================
    # VALIDATE STATUS CODE
    # ==========================================
    assert response.status_code == 200
    print("GET /events API successful")
    AllureReport.attach_text(f"GET /events API successful with status code {response.status_code}", "GET API Validation")

    # ========================================================
    # SWITCH TO ANYPOINT TAB
    # ========================================================

    driver.switch_to.window(
        driver.anypoint_tab
    )
    # ==========================================
    # VALIDATE GET API LOGS
    # ==========================================

    runtime_manager_page.goto_runtime_verify_latest_logs_matched(response.status_code,"savourypastry");
