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
@allure.story("Schema validation failure")
@allure.severity(allure.severity_level.NORMAL)
def test_ASB_message_with_invalid_schema(driver):

    api = APICalls()

    asb_connection_string = ConfigReader.get_api_config("ASB_CONNECTION_STRING")
    asb_helper = AzureServiceBusHelper(asb_connection_string)
    runtime_manager_page = RuntimeManager(driver)
    fresh_service_incident_page = FreshServiceIncidentPage(driver)

    # ==========================================
    # BUILD PAYLOAD
    # ==========================================
    payload_str, event_id, input_time = api.get_payload("wrong_schema.json")
    print(f"Generated Event ID: {event_id}")
    print(f"Generated Input time: {input_time}")

    #Send ASB message with wrong schema
    asb_helper.send_message_to_topic(payload_str, "com.sb.npd.rp.topic")

    # ========================================================
    # SWITCH TO ANYPOINT TAB
    # ========================================================
    driver.switch_to.window(
        driver.anypoint_tab
    )
    runtime_manager_page.goto_runtime_verify_logs_invalid_msg_received("400","message-acknowledged-due-to-invalid-input")

    # ========================================================
    # SWITCH TO FRESH SERVICE TAB
    # ========================================================
    driver.switch_to.window(
        driver.freshservice_tab
    )
    fresh_service_incident_page.search_and_capture_incident(event_id, "MuleSoft Technical Error")
