import json
import time

from azure.servicebus import ServiceBusClient
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from utilities.allure_report import AllureReport
from utilities.base import BasePage
from utilities.browser_manager import BrowserManager
from utilities.config_reader import ConfigReader
from utilities.data_generator import DataGenerator
from utilities.file_reader import FileReader


class ServiceBusExplorer(BasePage):

    TOPICS_MENU = By.XPATH,"//div[normalize-space()='Topics']"
    SEARCH_BOX_TO_FILTER_ITMES = By.CSS_SELECTOR,"input[placeholder='Search to filter items by name...']"
    TOPIC_ENTITIES_BUTTON = By.XPATH,"(//div[contains(@class,'azc-group-entitiesgroup')]//button)[2]"
    SUBSCRIPTIONS_MENU = By.XPATH,"//div[@data-telemetryname='Menu-subscriptions']"
    SERVICE_BUS_EXPLORER = By.XPATH,"(//div[@data-telemetryname='Menu-explorer'])[1]"
    SUBS_SERVICE_BUS_EXPLORER = By.XPATH, "(//div[@data-telemetryname='Menu-explorer'])[2]"
    PEEK_FROM_START_BUTTON = By.XPATH,"//button[.//span[normalize-space()='Peek from start']]"
    LAST_MESSAGE_CHECKBOX = By.XPATH,"(//div[@aria-label='Select message'])[last()]"
    MESSAGE_BODY = By.XPATH,"//div[contains(@class,'message-body')]"
    SEND_MESSAGES_BUTTON =  By.XPATH, "//button[.//span[normalize-space()='Send messages']]"
    CONTENT_TYPE_DROPDOWN = By.XPATH, "//div[@role='combobox']"
    APPLICATION_JSON_OPTION = By.XPATH,"//span[normalize-space()='application/json']"
    MESSAGE_EDITOR = By.XPATH,"//div[contains(@class,'view-line')]"
    SEND_BUTTON = By.XPATH,"//button[.//span[normalize-space()='Send']]"
    COMPLETED_TOAST_MESSAGE = By.XPATH,"//*[contains(text(),'Completed')]"
    SERVICE_BUS_EXPLORER_FRAME = By.XPATH,"//*[@name='ServiceBusExplorer.ReactView']"
    SUBSCRIPTIONS_MESSAGES_GRID_FRAME = By.XPATH,"(//*[@name='ServiceBusExplorer.ReactView'])[1]"



    def __init__(self, driver):
        super().__init__(driver)


    def navigate_to_topics(self):
        self.click(self.TOPICS_MENU,"Topics Menu")
        #time.sleep(2)  # Wait for the page to load


    def search_topic(self, topic_name):
        self.enter_text(self.SEARCH_BOX_TO_FILTER_ITMES, topic_name, "Search Box to filter items..")
       # time.sleep(2)  # Wait for search results to update

    def get_topic_link(self,topic_name):
        return (By.XPATH, f"//a[normalize-space()='{topic_name}']")

    def verify_topic_displayed(self, topic_name):
        topic_locator = self.get_topic_link(topic_name)

        visible = self.is_element_visible(
            topic_locator,
            f"Topic Link: {topic_name}"
        )

        assert visible, (
            f"Topic '{topic_name}' is not displayed"
        )

        print(
            f"Verified topic '{topic_name}' is displayed"
        )

    def click_on_topic(self, topic_name):
        topic_locator = self.get_topic_link(topic_name)

        self.click(
            topic_locator,
            f"Topic Link: {topic_name}"
        )

        print(
            f"Clicked on topic: {topic_name}"
        )

    def click_entities_button(self):
        self.is_element_visible(
            self.TOPIC_ENTITIES_BUTTON,
            "Expand Entities Button"
        )
        element = self.driver.find_element(
            *self.TOPIC_ENTITIES_BUTTON
        )
        # JS click
        self.driver.execute_script("arguments[0].click();",element)

        print("Clicked Expand Entities Button")
        #self.click(self.TOPIC_ENTITIES_BUTTON,"Expand Entities Button")

    def click_subscriptions_menu(self):
        self.click(self.SUBSCRIPTIONS_MENU,"Subscriptions Menu")

    def click_Subscription_service_bus_explorer(self):
        self.click(self.SUBS_SERVICE_BUS_EXPLORER,"Service Bus Explorer Menu")

    def click_peek_from_start(self):

        self.switch_to_frame(self.SERVICE_BUS_EXPLORER_FRAME)

        element = self.wait_until_enabled(
            self.PEEK_FROM_START_BUTTON,
            "Peek From Start Button"
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            element
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        print("Clicked on Peek From Start Button")



    def goto_asb_topic_verify_message_presence(self, topic,subscription, expected_message):
        self.search_topic(topic)
        # Verify topic displayed
        self.verify_topic_displayed(topic)

        # Click topic
        self.click_on_topic(topic)

        # Click entities → subscriptions → service bus explorer
        self.click_entities_button()
        self.click_subscriptions_menu()
        self.click_on_topic(subscription)
        self.click_Subscription_service_bus_explorer()

        # Click peek from start
        self.click_peek_from_start()

        self.select_last_message_and_verify_event_id(expected_message)

    def select_last_message_and_verify_event_id(self,expected_message):

        self.scroll_message_grid_to_bottom()

        # Scroll to checkbox
        # self.scroll_into_view(self.LAST_MESSAGE_CHECKBOX,"Last Message Checkbox")
        # time.sleep(0.5)
        # self.scroll_into_view(self.LAST_MESSAGE_CHECKBOX, "Last Message Checkbox")
        # time.sleep(0.5)
        checkbox_element = self.scroll_into_view(self.LAST_MESSAGE_CHECKBOX, "Last Message Checkbox")
        # time.sleep(0.5)
        # print("Scrolled to last message checkbox")

        # Click checkbox
        #checkbox_element.click()
        self.driver.execute_script("arguments[0].click();",checkbox_element)
        print("Clicked last message checkbox")

        # Wait for message body
        visible = self.is_element_visible(self.MESSAGE_BODY,"Message Body")

        assert visible,("Message body not displayed")

        # Get message body text
        message_body_text = self.get_text(self.MESSAGE_BODY,"Message Body")

        print("========= MESSAGE BODY =========")
        print(message_body_text)
        AllureReport.attach_text(message_body_text, "Message Body")

        # Verify event id
        assert expected_message in message_body_text, (
            f"Event ID '{expected_message}' "
            f"not found in message body"
        )
        print( f"Verified Event ID " f"'{expected_message}' " f"present in message body" )
        # Save screenshot directly
        screenshot_path = self.take_screenshot(f"ASB message body {expected_message}.png")
        # Attach screenshot to Allure
        AllureReport.attach_screenshot(
            screenshot_path,
            "Runtime Manager Logs Screenshot"
        )

    def goto_asb_topic_send_message_get_event_id(self, topic):

        self.search_topic(topic)
        # Verify topic displayed
        self.verify_topic_displayed(topic)

        # Click topic
        self.click_on_topic(topic)

        self.click_subscriptions_menu()


        # Click entities → subscriptions → service bus explorer
        self.click_entities_button()

        self.click_service_bus_explorer()

        # Click peek from start
        self.click_peek_from_start()

        #send message to topic and get event id
        event_id = self.send_message_verify_posted_successfully()

        return event_id

    def click_send_button(self):
        send_button = self.scroll_into_view(
            self.SEND_BUTTON,"Send Button")

        self.driver.execute_script( "arguments[0].click();",send_button)

        print("Clicked on Send button")

    def send_message_verify_posted_successfully(self):
        # ==========================================
        # READ JSON FILE
        # ==========================================
        file_reader = FileReader()

        file_reader = FileReader()

        # ==========================================
        # CONFIG VALUES
        # ==========================================
        client_id = ConfigReader.get_api_config("CLIENT_ID")
        client_secret = ConfigReader.get_api_config("CLIENT_SECRET")

        # ==========================================
        # TEST DATA
        # ==========================================
        payload = file_reader.read_json("create_event.json")
        payload["id"] = DataGenerator.generate_event_id()
        payload["time"] = DataGenerator.generate_current_timestamp()

        event_id = payload["id"]

        print(f"Generated Event ID: {event_id}")

        # ==========================================
        # CONVERT TO JSON STRING
        # ==========================================
        json_payload = json.dumps(
            payload,
            indent=2
        )

        self.click(self.SEND_MESSAGES_BUTTON, "Send Messages Button")
        print("Clicked Send Messages button")

        self.click(self.CONTENT_TYPE_DROPDOWN, "Content Type Dropdown")
        self.click(self.APPLICATION_JSON_OPTION, "application/json) option")

        # ==========================================
        # CLICK MESSAGE EDITOR
        # ==========================================
        editor = self.scroll_into_view(
            self.MESSAGE_EDITOR,
            "Message Editor"
        )

        actions = ActionChains(self.driver)

        actions.click(editor)

        # Clear existing content
        actions.key_down(Keys.CONTROL)
        actions.send_keys("a")
        actions.key_up(Keys.CONTROL)

        actions.send_keys(json_payload)

        actions.perform()

        print("JSON payload entered successfully")

        self.click_send_button()
        self.verify_completed_toast_message()

        # ==========================================
        # RETURN EVENT ID
        # ==========================================
        return event_id

    def verify_completed_toast_message(self):
        self.is_element_visible(self.COMPLETED_TOAST_MESSAGE,"Completed Toast Message")

        toast_text = self.get_text(
            self.COMPLETED_TOAST_MESSAGE,
            "Completed Toast Message"
        )
        assert "Completed" in toast_text, (
            f"Expected 'Completed' message "
            f"but got '{toast_text}'"
        )
        print(
            f"Toast message verified successfully: "
            f"{toast_text}"
        )

    def gradual_scroll_message_grid(self):

        last_height = 0

        while True:

            current_height = self.driver.execute_script("""
                let grid = document.querySelector(
                    '.ms-List-surface'
                );

                grid.scrollTop = grid.scrollHeight;

                return grid.scrollHeight;
            """)

            if current_height == last_height:
                break

            last_height = current_height

            time.sleep(2)

        print("Completed grid scroll")

    def get_last_and_click(self, max_scrolls=10):
        last_row = None

        for _ in range(max_scrolls):
            rows = self.driver.find_elements(By.XPATH, "//div[@aria-label='Select message']")

            if rows:
                last_row = rows[-1]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", last_row)

                time.sleep(1)  # wait for lazy loading

        if last_row:
            last_row.click()
        else:
            raise Exception("No rows found")

    def scroll_message_grid_to_bottom(self):

        self.driver.execute_script("""
            let grid = document.querySelector('.ms-ScrollablePane--contentContainer contentContainer-206');

            if(grid){
                grid.scrollTop = grid.scrollHeight;
            }
        """)

        print("Scrolled message grid to bottom")


    def verify_asb_topic(self):
        from azure.servicebus import ServiceBusClient

        CONNECTION_STR = "Endpoint=sb://sb-integrations-dev-servicebus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=23gK8uqgiw/PJHu2aj95dPCv+nnL7W9Ck8/Xikjxn5E="
        TOPIC_NAME = "com.sb.rp.npd.topic"
        SUBSCRIPTION_NAME = "com.sb.rp.npd.subs"

        client = ServiceBusClient.from_connection_string(CONNECTION_STR)

        with client:
            receiver = client.get_subscription_receiver(
                topic_name=TOPIC_NAME,
                subscription_name=SUBSCRIPTION_NAME
            )

            with receiver:
                peeked_msgs = receiver.peek_messages()

                for msg in peeked_msgs:
                    print("Message:", str(msg))

    from azure.servicebus import ServiceBusClient

    def peek_all_messages(self,connection_str, topic, subscription, batch_size=50):
        client = ServiceBusClient.from_connection_string(connection_str)

        all_messages = []
        last_seq = 0

        with client:
            receiver = client.get_subscription_receiver(
                topic_name=topic,
                subscription_name=subscription
            )

            with receiver:
                while True:
                    batch = receiver.peek_messages(
                        max_message_count=batch_size,
                        sequence_number=last_seq
                    )

                    if not batch:
                        break

                    for msg in batch:
                        all_messages.append(msg)
                        last_seq = msg.sequence_number + 1

        return all_messages
