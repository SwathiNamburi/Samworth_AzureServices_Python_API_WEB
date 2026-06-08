import time

from selenium.webdriver.common.by import By
from utilities.base import BasePage
from utilities.browser_manager import BrowserManager
from utilities.config_reader import ConfigReader


class DATAExplorerHomePage(BasePage):
    EMAIL_INPUT = By.XPATH, "//input[@type='email']"
    SUBMIT_BUTTON = By.XPATH, "//input[@type='submit']"
    PASSWORD_INPUT = By.XPATH, "//input[@type='password']"
    SMS_OPTION = By.CSS_SELECTOR, "div[data-value='OneWaySMS']"
    PAGE_TITLE = By.XPATH, "(//h2[contains(@class,'fxs-blade-title-titleText')])[1]"

    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigReader()
        self.tenant = ConfigReader.get_ui_config("TENANT")
        self.username = ConfigReader.get_ui_config("USERNAME")
        self.password = ConfigReader.get_ui_config("PASSWORD")

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email, "Email Input")

    def click_next(self):
        self.click(self.SUBMIT_BUTTON, "Next Button")

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password, "Password Input")

    def click_sign_in(self):
        self.click(self.SUBMIT_BUTTON, "Sign In Button")

    def select_sms_option(self):
        self.click(self.SMS_OPTION, "One Way SMS Option")

    def verify_topics_page_title(self, expected_title):
        actual_title = self.get_text(
            self.PAGE_TITLE,
            "Topics Page Title"
        )
        print(f"Actual Title: {actual_title}")

        assert expected_title in actual_title, (
            f"Expected title '{expected_title}' "
            f"not found in '{actual_title}'"
        )
        print("Topics page title verified successfully")


    def login_to_asb_portal(self):
        asb_url = ConfigReader.get_ui_config("ASB_PORTAL_URL")

        self.driver.get(asb_url)
        self.enter_email(self.config.get_ui_config("USERNAME"))
        self.click_next()
        self.enter_password(self.config.get_ui_config("PASSWORD"))
        self.click_sign_in()
        self.select_sms_option()
        # waits.wait_for_manual_input(30, "Please complete the manual input.")
        time.sleep(30)
        self.verify_topics_page_title("Topics")

