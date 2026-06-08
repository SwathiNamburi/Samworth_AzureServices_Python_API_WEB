import time

from selenium.webdriver.common.by import By

from utilities.allure_report import AllureReport
from utilities.base import BasePage
from utilities.browser_manager import BrowserManager
from utilities.config_reader import ConfigReader


class FreshServiceHomepage(BasePage):
    EMAIL_INPUT = By.XPATH, "//input[@type='email']"
    SUBMIT_BUTTON = By.XPATH, "//input[@type='submit']"
    PASSWORD_INPUT = By.XPATH, "//input[@type='password']"
    #SMS_OPTION = By.CSS_SELECTOR, "div[data-value='OneWaySMS']"
    ACCOUNT_ELEMENT = By.XPATH,"//a[contains(@aria-label,'Profile settings')]"

    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigReader()
        self.fresh_service_username = ConfigReader.get_ui_config("Fresh_Service_Username")
        self.fresh_service_password = ConfigReader.get_ui_config("Fresh_Service_Password")

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email, "Email Input")

    def click_next(self):
        self.click(self.SUBMIT_BUTTON, "Next Button")

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password, "Password Input")

    def click_sign_in(self):
        self.click(self.SUBMIT_BUTTON, "Sign In Button")

    def navigate_to_fresh_service_portal(self):
        fresh_service_url = ConfigReader.get_ui_config("Fresh_Service_URL")

        self.driver.get(fresh_service_url)
        self.enter_email(self.fresh_service_username)
        self.click_next()
        self.enter_password(self.fresh_service_password)
        self.click_sign_in()
        #self.select_sms_option()
        # waits.wait_for_manual_input(30, "Please complete the manual input.")
        time.sleep(30)
        self.verify_fresh_service_home_page_title()
        AllureReport.attach_text("Logged in to Fresh Service Platform successfully",
            "Navigated to Fresh Service platform"
        )

    def verify_fresh_service_home_page_title(self):
        self.is_element_visible(self.ACCOUNT_ELEMENT,"Account Element")
        #AllureReport.attach_text("Navigated to Fresh Service Portal","")




