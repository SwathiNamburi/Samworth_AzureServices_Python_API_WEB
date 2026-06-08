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
@allure.feature("ASB Consume")
@allure.story("Valid ASB message")
@allure.severity(allure.severity_level.CRITICAL)
def test_asb_consume_message_received_cosmosdb(driver):

    api = APICalls()

    asb_connection_string = ConfigReader.get_api_config("ASB_CONNECTION_STRING")
    asb_helper = AzureServiceBusHelper(asb_connection_string)
    cosmos_helper = CosmosDBHelper()
    runtime_manager_page = RuntimeManager(driver)

    # ==========================================
    # BUILD PAYLOAD
    # ==========================================
    payload_str, event_id, input_time = api.get_payload("create_event.json")
    print(f"Generated Event ID: {event_id}")

    # ==========================================
    # SEND MESSAGE TO TOPIC
    # ==========================================
    asb_helper.send_message_to_topic(payload_str,"com.sb.npd.rp.topic")

    # ==========================================
    # STORE EVENT ID FOR FURTHER VALIDATION
    # ==========================================
    response_event_id = event_id
    print(
        f"Stored Event ID: "
        f"{response_event_id}"
    )
    assert response_event_id is not None


    # ==========================================
    # FETCH MESSAGE FROM COSMOS DB
    # ==========================================
    cosmos_message = cosmos_helper.get_message_by_event_id(event_id)
    print("Fetched Cosmos DB Message:")
    print(cosmos_message)

    # ==========================================
    # VALIDATE EVENT ID
    # ==========================================
    assert cosmos_message["id"] == event_id, (
        f"Expected Event ID '{event_id}' "
        f"not found in Cosmos DB"
    )

    print(
        f"Cosmos DB validation successful "
        f"for Event ID: {event_id}"
    )
    AllureReport.attach_text(f"Cosmos DB received matched ASB message with Event ID: {event_id}", "Cosmos DB Validation")

    # ==========================================
    # EXTRACT DATA FROM COSMOS DB MESSAGE
    # ==========================================

    event_data = cosmos_message["data"][0]

    tenant_id = event_data["tenantid"]

    event_time = event_data["time"]

    response_event_id = event_data["id"]

    print(f"Tenant ID : {tenant_id}")
    print(f"Event Time: {event_time}")
    print(f"Event ID  : {response_event_id}")

    # ==========================================
    # GET EVENTS API CALL
    # ==========================================

    response, response_body = api.get_events_api_call(
        start_time=input_time,
        tenant_id=tenant_id
    )
    # ==========================================
    # VALIDATE STATUS CODE
    # ==========================================
    assert response.status_code == 200
    print("GET /events API successful")
    AllureReport.attach_text(f"GET /events API successful with status code {response.status_code}", "GET API Validation")


    # ==========================================
    # VALIDATE EVENT ID IN RESPONSE
    # ==========================================
    response_ids = [
        item["id"]
        for item in response_body
    ]
    assert response_event_id in response_ids, (
        f"Event ID '{response_event_id}' "
        f"not found in GET API response"
    )
    print(
        f"Validated Event ID "
        f"{response_event_id} in GET response"
    )

    # ========================================================
    # SWITCH TO ANYPOINT TAB
    # ========================================================

    driver.switch_to.window(
        driver.anypoint_tab
    )
    # ==========================================
    # VALIDATE GET API LOGS
    # ==========================================
    runtime_manager_page.goto_runtime_verify_post_logs_matched(response.status_code,response_event_id)
