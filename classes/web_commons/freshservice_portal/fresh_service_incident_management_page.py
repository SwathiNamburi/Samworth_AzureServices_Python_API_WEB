import time
from selenium.webdriver.common.by import By

from utilities.allure_report import AllureReport
from utilities.base import BasePage
from utilities.config_reader import ConfigReader


class FreshServiceIncidentPage(BasePage):
    SEARCH_INPUT = By.XPATH,"//input[@name='term' and @placeholder='Search']"
    SEARCH_RESULT = By.CSS_SELECTOR,"a.search-title"
    INCIDENT_ID = By.XPATH,"//span[@data-test-id='ticket-human-display-id']"
    ALERT_LINK = By.CSS_SELECTOR,"a.search-title"
    SUBJECT_LABEL = By.XPATH,"//span[text()='Subject']"





    def __init__(self, driver):
        super().__init__(driver)


    def search_incident(self, entity_name):
        #self.clear_text(self.SEARCH_INPUT)
        fresh_service_url = ConfigReader.get_ui_config("Fresh_Service_URL")
        self.driver.get(fresh_service_url)
        time.sleep(2)
       # self.is_element_visible(self.SUBJECT_LABEL,"Subject label")
        self.enter_text(self.SEARCH_INPUT, entity_name, "Search Input")

    def click_search_result(self):
        self.click(self.SEARCH_RESULT,"Search Result")
        print("Clicked on search result")

    def get_incident_id(self):
        incident_id = self.get_text(self.INCIDENT_ID,"Incident ID")
        print(f"Incident ID: {incident_id}")
        return incident_id

    def get_alert_link_text(self):
        alert_link_text = self.get_text(self.ALERT_LINK, "Alert link Text")
        print(f"Alert info: {alert_link_text}")
        return alert_link_text

    def open_alert_with_link(self):
        self.click(self.ALERT_LINK, "Alert link")
        print("Clicked on alert link")
        time.sleep(2)

    def capture_incident_screenshot(self,incident_id):

        screenshot_path = self.take_screenshot("incident_page")
        print(f"Incident screenshot captured: " f"{screenshot_path}")

        return screenshot_path

    def search_and_capture_incident(self,search_input,alert_detail):
        self.refresh_and_wait(30)
        time.sleep(5)
        print(f"search_input: " f"{search_input}")
        # Search with event ID
        self.search_incident(search_input)
        self.press_enter()
        time.sleep(3)
        # Click search result
        #self.click_search_result()

        # Get alert info text
        alert_info = self.get_alert_link_text()

        # Validate alert detail exists in alert info
        assert alert_detail in alert_info, (
            f"Alert detail '{alert_detail}' not found in Alert Info"
        )

        # Extract only incident ID from alert info
        # Example:
        # "MuleSoft Technical Error required key [source] not found #Alert-7261"

        incident_id = alert_info.split("#")[-1].strip()

        print(f"Incident ID: {incident_id}")

        self.open_alert_with_link()

        # Capture screenshot
        screenshot_path = self.capture_incident_screenshot(
            incident_id.replace("Alert-", "")
        )
        AllureReport.attach_screenshot(
            screenshot_path,
            "Fresh Service Alert Screenshot"
        )

        # Attach details to Allure
        AllureReport.attach_text(
            "Alert Created with ID",
            incident_id
        )

        AllureReport.attach_text(
            "Alert detail",
            alert_info
        )


        return incident_id, screenshot_path
