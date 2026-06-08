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
@allure.feature("ASB Consume")
@allure.story("Cosmos DB Failure")
@allure.severity(allure.severity_level.CRITICAL)
def test_cosmosdb_failure_with_incorrect_setting(driver):

    api = APICalls()

    asb_connection_string = ConfigReader.get_api_config("ASB_CONNECTION_STRING")
    asb_helper = AzureServiceBusHelper(asb_connection_string)
    cosmos_helper = CosmosDBHelper()
    runtime_manager_page = RuntimeManager(driver)
    fresh_service_incident_page = FreshServiceIncidentPage(driver)

    # ==========================================
    # BUILD PAYLOAD
    # ==========================================
    payload_str, input_event_id, input_time = api.get_payload("create_event.json")
    print(f"Generated Event ID: {input_event_id}")

    # ==========================================
    # SEND MESSAGE TO TOPIC
    # ==========================================
    asb_helper.send_message_to_topic(payload_str,"com.sb.npd.rp.topic")

    # ==========================================
    # STORE EVENT ID FOR FURTHER VALIDATION
    # ==========================================
    response_event_id = input_event_id
    print(
        f"Stored Event ID: "
        f"{response_event_id}"
    )
    assert response_event_id is not None

    # ==========================================
    # FETCH MESSAGE FROM COSMOS DB
    # ==========================================

    cosmos_message = cosmos_helper.verify_invalid_cosmodb_exception_failure(input_event_id)
    print("Fetched Cosmos DB Message:")
    print(cosmos_message)

    # ========================================================
    # SWITCH TO ANYPOINT TAB
    # ========================================================
    driver.switch_to.window(
        driver.anypoint_tab
    )
    # Select Runtime Manager and verify event ID in logs
    runtime_manager_page.goto_runtime_verify_logs_invalid_msg_received("404",input_event_id)  # Select Runtime Manager

    # ========================================================
    # SWITCH TO Fresh Service TAB
    # ========================================================
    driver.switch_to.window(
        driver.freshservice_tab
    )
    fresh_service_incident_page.search_and_capture_incident(input_event_id, "MuleSoft Technical Error")
