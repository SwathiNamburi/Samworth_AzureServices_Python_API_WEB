import os
import time

import requests
from selenium.webdriver.common.by import By

from utilities.allure_report import AllureReport
from utilities.base import BasePage
from utilities.browser_manager import BrowserManager
from utilities.config_reader import ConfigReader


class AnypointHomePage(BasePage):

    # Config details
    env_name = ConfigReader.get_api_config("ENV_NAME")
    anypoint_host = ConfigReader.get_api_config("ANYPOINT_HOST")
    logs_target_app_name = ConfigReader.get_api_config("TARGET_APP_NAME")
    barrier = ConfigReader.get_api_config("BEARER_TOKEN")

    USE_CUSTOM_DOMAIN = By.XPATH,"//a[@data-test-id='SignIn-CustomDomain']"
    CUSTOM_DOMAIN_INPUT = By.ID, "customDomainField"
    CONTINUE_BUTTON = By.XPATH, "//button[@type='submit']//span[text()='Continue']/ancestor::button"
    CONTINUE_WITH_MICROSOFT_SSO_BUTTON = By.XPATH,"//button[.//span[normalize-space()='Continue with Microsoft Entra SSO']]"
    EMAIL_INPUT = By.XPATH, "//input[@type='email']"
    SUBMIT_BUTTON = By.XPATH, "//input[@type='submit']"
    PASSWORD_INPUT = By.XPATH, "//input[@type='password']"
    #SIGN_IN_BUTTON = By.XPATH, "//input[@type='submit']"
    SIGN_IN_BTN = By.XPATH,"//button[@data-test-id='SignIn-Submit']"
    USERNAME_INPUT= By.ID, "nameInput"
    USER_PASSWORD_INPUT = By.ID, "passwordInput"
    USER_SIGN_IN_BUTTON = By.XPATH,"//button[@data-test-id='SignIn-Submit']"
    SMS_OPTION = By.CSS_SELECTOR, "div[data-value='OneWaySMS']"
    BUSINESS_GROUP_LABEL = By.XPATH,"//span[@title='Business Groups' and contains(text(),'Samworth Brothers')]"

    def __init__(self, driver):
        super().__init__(driver)
        self.tenant = ConfigReader.get_ui_config("TENANT")
        self.username = ConfigReader.get_ui_config("USERNAME")
        self.password = ConfigReader.get_ui_config("PASSWORD")

    def click_use_custom_domain(self):
        self.click(self.USE_CUSTOM_DOMAIN,"Use Custom Domain")

    def enter_custom_domain(self,custom_domain):
        self.enter_text(self.CUSTOM_DOMAIN_INPUT,custom_domain,"Custom Domain Input")

    def click_continue(self):
        self.click(self.CONTINUE_BUTTON,"Continue Button")

    def click_continue_with_microsoft_sso(self):
        self.click(self.CONTINUE_WITH_MICROSOFT_SSO_BUTTON,"Continue with Microsoft SSO Button")

    def enter_email(self,email):
        self.enter_text(self.EMAIL_INPUT,email,"Email Input")

    def click_next(self):
        self.click(self.SUBMIT_BUTTON,"Next Button")

    def enter_password(self,password):
        self.enter_text(self.PASSWORD_INPUT,password,"Password Input")

    def enter_username(self,username):
        self.enter_text(self.USERNAME_INPUT,username,"Username Input")

    def enter_user_password(self,password):
        self.enter_text(self.USER_PASSWORD_INPUT,password,"Password Input")

    def click_user_sign_in(self):
        self.click(self.USER_SIGN_IN_BUTTON,"Sign In Button")

    def click_sign_in(self):
        self.click(self.SUBMIT_BUTTON,"Sign In Button")

    def select_sms_option(self):
        self.click(self.SMS_OPTION,"One Way SMS Option")

    def verify_successful_login(self):
        visible = self.is_element_visible(
            self.BUSINESS_GROUP_LABEL,
            "Business Group Label"
        )
        assert visible, "Login failed - Business Group not visible"
        print("Login successful, Business Groups label is visible.")

    def login_with_microsoft_sso(self):
        self.click_use_custom_domain()
        self.enter_custom_domain(self.tenant)
        self.click_continue()
        self.click_continue_with_microsoft_sso()
        self.enter_email(self.username)
        self.click_next()
        self.enter_password(self.password)
        self.click_sign_in()
        self.select_sms_option()
        #waits.wait_for_manual_input(30, "Please complete the manual input.")
        time.sleep(30)
        self.verify_successful_login()

    def login_without_microsoft_sso(self):
        self.enter_username(self.username)
        self.enter_user_password(self.password)
        self.click_user_sign_in()
        #waits.wait_for_manual_input(30, "Please complete the manual input.")
        time.sleep(20)
        self.verify_successful_login()
        AllureReport.attach_text("Logged in to Anypoint Platform successfully",
            "Login to Anypoint Platform"
        )




    def login_to_anypoint_platform(self):

        anypoint_url = ConfigReader.get_ui_config("Anypoint_Platform_URL")
        self.driver.get(anypoint_url)

        # Login with Microsoft SSO using test credentials
        #self.login_with_microsoft_sso()
        self.login_without_microsoft_sso()


    # --- Configuration Settings ---

    def get_org_and_env_ids(self,token):

        host=self.anypoint_host
        """Step 1: Get Organization ID and Environment ID."""
        headers = {"Authorization": f"Bearer {token}"}
        print("🏢 Retrieving Profile details...")
        profile_res = requests.get(f"{host}/accounts/api/profile", headers=headers)
        profile_res.raise_for_status()
        profile_data = profile_res.json()
        org_id = profile_data.get("organization", {}).get("id")

        env_id = None
        for env in profile_data.get("organization", {}).get("environments", []):
            if env.get("name").lower() == self.env_name.lower():
                env_id = env.get("id")
                break

        if not env_id:
            raise ValueError(f"Could not find environment '{self.env_name}'")
        return org_id, env_id

    def get_application_ids(self,token, org_id, env_id):
        """Step 2 & 3: Find the deployment, then fetch individual details for the specificationId."""
        headers = {"Authorization": f"Bearer {token}"}
        list_url = f"{self.anypoint_host}/amc/application-manager/api/v2/organizations/{org_id}/environments/{env_id}/deployments"

        print(f"🔍 Locating '{self.logs_target_app_name}' in list...")
        list_res = requests.get(list_url, headers=headers)
        list_res.raise_for_status()

        deployment_id = None
        for app in list_res.json().get("items", []):
            if app.get("name").lower() == self.logs_target_app_name.lower():
                deployment_id = app.get("id")
                break

        if not deployment_id:
            raise ValueError(f"Application '{self.logs_target_app_name}' was not found in environment '{self.env_name}'.")

        # --- FIX: Fetch the individual deployment directly to get the true specificationId ---
        print(f" Fetching deep deployment details for ID: {deployment_id}...")
        detail_url = f"{list_url}/{deployment_id}"
        detail_res = requests.get(detail_url, headers=headers)
        detail_res.raise_for_status()
        detail_data = detail_res.json()

        # Check alternative key mappings where CloudHub 2.0 stores this value
        spec_id = detail_data.get("application", {}).get("specificationId") or detail_data.get("desiredVersion")

        if not spec_id:
            raise ValueError("Failed to retrieve a valid specificationId or desiredVersion from the MuleSoft API.")

        return deployment_id, spec_id

    def download_ch2_logs(self,token, org_id, env_id, deployment_id, spec_id):
        """Step 4: Pull logs file."""
        log_url = (
            f"{self.anypoint_host}/amc/application-manager/api/v2"
            f"/organizations/{org_id}/environments/{env_id}"
            f"/deployments/{deployment_id}/specs/{spec_id}/logs/file"
        )
        headers = {"Authorization": f"Bearer {token}", "Accept": "text/plain"}

        print("⏳ Downloading log stream...")
        response = requests.get(log_url, headers=headers)
        response.raise_for_status()
        return response.text

    def verify_log_event(self,log_file_path,target_id):
        print(f"\n🔍 Starting automated assertion for ID: {target_id}")

        with open(log_file_path, "r", encoding="utf-8") as f:
            log_content = f.read()

        # --- Assertion : Basic text presence check ---
        assert target_id in log_content, f"❌ Test Failed: ID '{target_id}' was not found anywhere in the logs!"
        print(f"✅ Pass: Found {target_id} ID in log file.")


    def verify_anypoint_logs_events(self, target_id):
        try:
            token = self.barrier
            # Resolve Context IDs
            org_id, env_id = self.get_org_and_env_ids(token)
            print(f"✅ Resolved Context | Org: {org_id} | Env: {env_id}")

            # Get Deployment and the missing Spec IDs
            deployment_id, spec_id = self.get_application_ids(self.barrier, org_id, env_id)
            print(f"✅ Target Identified | Deployment ID: {deployment_id} | Spec ID: {spec_id}")

            # Pull Down Log File
            logs_data = self.download_ch2_logs(self.barrier, org_id, env_id, deployment_id, spec_id)

            writefile=os.path.join(os.getcwd(),"testdata\\runtime_files")
            output_filename = f"{writefile}\\{self.logs_target_app_name}_cloudhub2.log"
            with open(output_filename, "w", encoding="utf-8") as file:
                file.write(logs_data)

            print(f" Success! Logs saved to local file: '{output_filename}'")

            # Point this to the log file downloaded by your script execution
            LOG_FILE_PATH = output_filename
            TARGET_ID = target_id

            try:
                self.verify_log_event(LOG_FILE_PATH, TARGET_ID)
            except AssertionError as msg:
                print(msg)

        except Exception as err:
            print(f"❌ Execution failed: {err}")










