import allure
import pytest

from classes.api_commons.api_calls import APICalls
from classes.db_commons.cosmos_db.cosmos_helper import CosmosDBHelper
from classes.mq_commons.abs.asb_helper import AzureServiceBusHelper
from classes.web_commons.anypoint_platform.anypoint_homepage import AnypointHomePage
from classes.web_commons.anypoint_platform.runtime_manager_page import RuntimeManager
from classes.web_commons.freshservice_portal.fresh_service_homepage import FreshServiceHomepage
from classes.web_commons.freshservice_portal.fresh_service_incident_management_page import FreshServiceIncidentPage
from utilities.allure_report import AllureReport
from utilities.config_reader import ConfigReader

@pytest.mark.smoke
@allure.feature("Get Events")
@allure.story("Invalid Date Format")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_events_with_invalid_date_format(driver):

    api = APICalls()

    asb_connection_string = ConfigReader.get_api_config("ASB_CONNECTION_STRING")
    asb_helper = AzureServiceBusHelper(asb_connection_string)
    runtime_manager_page = RuntimeManager(driver)
    fresh_service_incident_page = FreshServiceIncidentPage(driver)

    # ==========================================
    # BUILD PAYLOAD
    # ==========================================
    payload_str, event_id, input_time = api.get_payload("create_event.json")
    print(f"Generated Event ID: {event_id}")
    print(f"Generated Input time: {input_time}")
    invalid_date_time = input_time.replace("Z", "T")
    print(invalid_date_time)

    asb_helper.send_message_to_topic(payload_str, "com.sb.npd.rp.topic")

    # ==========================================
    # GET EVENTS API CALL
    # ==========================================
    #start_time = input_time
    response, response_body = api.get_events_api_call_with_invalid_date_format(invalid_date_time,tenant_id="savourypastry")
    response_instance_id = response_body["instance"]
    response_status = response_body["status"]

    # Extract only first error line
    detail_message = response_body["detail"]
    expected_alert_msg = detail_message.split(".")[1]
    print(expected_alert_msg)
    print(f"details: {expected_alert_msg}")
    print(f"instance id: {response_instance_id}")
    print(f"status: {response_status}")
    # ==========================================
    # VALIDATE STATUS CODE
    # ==========================================
    assert response.status_code == 400
    print("GET /events API successfully returned status code 400 for missing start_time parameter.")
    AllureReport.attach_text(f"GET /events API successful with status code {response.status_code}", "GET API Validation with missing start time")

    # ========================================================
    # SWITCH TO ANYPOINT TAB
    # ========================================================
    driver.switch_to.window(
        driver.anypoint_tab
    )
    # ==========================================
    # VALIDATE GET API LOGS
    # ==========================================
    runtime_manager_page.goto_runtime_verify_logs_instance_id_matched(response_status, response_instance_id,"Bad request")

    # ========================================================
    # SWITCH TO FRESH SERVICE TAB
    # ========================================================
    driver.switch_to.window(
        driver.freshservice_tab
    )

    fresh_service_incident_page.search_and_capture_incident(response_instance_id, expected_alert_msg)
