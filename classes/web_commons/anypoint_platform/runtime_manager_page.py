import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from utilities.allure_report import AllureReport
from utilities.base import BasePage
from utilities.config_reader import ConfigReader


class RuntimeManager(BasePage):

    RUNTIMES_DROPDOWN = By.CSS_SELECTOR, "span[data-test-id='navbar-products-runtimes-dropdown']"
    RUNTIME_MANAGER = By.CSS_SELECTOR,"li[data-test-id='navbar-list-item-Runtime-Manager'] a"
    DEVELOP_ENVIRONMENT = By.XPATH,"//div[contains(@class,'environments-row') and .//div[normalize-space()='Develop']]"
    SEARCH_APPLICATION_INPUT = By.XPATH,"//input[@data-test-id='search-applications-input']"
    APPLICATION_LINK = By.CSS_SELECTOR,"a[data-test-id='application-link']"
    LOGS_TAB = By.XPATH,"//a[@ui-sref='console.applications.domain.log' and normalize-space()='Logs']"
    LOG_SEARCH_INPUT = By.CSS_SELECTOR,"input[data-test-id='logs-omnibar-text-field-input']"
    LOG_MESSAGE_CONTAINER = By.XPATH,"(//pre[contains(@class,'LogMessageContainer')])[2]"
    LOG_SEARCH_ALERT_MESSAGE_CONTAINER = By.XPATH, "(//pre[contains(@class,'LogMessageContainer')])[3]"
    ERROR_LOG_MESSAGE = By.XPATH,"(//pre[contains(.,'Bad request error response received')])[1]"
    INFO_ALERT_LOG_MESSAGE = By.XPATH,"(//pre[contains(text(), 'Alert message published to alert queue')])[2]"
    EXCEPTION_LOG_MESSAGE = By.XPATH,"(//pre[contains(.,'Exception during exception strategy execution')])[1]"
    INVALID_INPUT_LOG_MSG = By.XPATH,"(//pre[contains(., 'message-acknowledged-due-to-invalid-input')])[1]"


    def __init__(self, driver):
        super().__init__(driver)


    def select_runtime_manager(self):
        self.click(self.RUNTIMES_DROPDOWN,"Runtimes Dropdown")
        self.click(self.RUNTIME_MANAGER,"Runtime Manager Option")

    def get_application_link(self, app_name):
        return (
            By.XPATH,
            f"//a[@data-test-id='application-link' "
            f"and normalize-space()='{app_name}']"
        )

    def navigate_to_runtime_application(self):

        app_name = ConfigReader.get_ui_config("Runtime_Manager_App")
        # ====================================================
        # SELECT RUNTIME MANAGER
        # ====================================================

        self.select_runtime_manager()

        # ====================================================
        # SELECT DEVELOP ENVIRONMENT
        # ====================================================

        self.click(
            self.DEVELOP_ENVIRONMENT,
            "Develop Environment"
        )

        # ====================================================
        # SEARCH APPLICATION
        # ====================================================

        self.enter_text(
            self.SEARCH_APPLICATION_INPUT,
            app_name,
            "Search Application Input"
        )

        application_locator = (
            self.get_application_link(app_name)
        )

        self.click(
            application_locator,
            f"Application: {app_name}"
        )

        self.wait_for_page_load()

        time.sleep(3)

        AllureReport.attach_text(
            f"Navigated to Runtime Manager "
            f"Application: {app_name}",
            "Runtime Manager Navigation"
        )

    def goto_runtime_verify_logs_instance_id_matched( self,response_status,expected_instance_id,
            expected_log_info):

        self.refresh_and_wait(30)
        time.sleep(5)
        self.click(self.LOGS_TAB, "Logs Tab")
        time.sleep(3)
        self.refresh_and_wait(15)
        # ==========================================
        # SUCCESS RESPONSE VALIDATION
        # ==========================================
        if str(response_status) in "Accepted" or str(response_status) in "200":

            log_info = self.get_logs_message(expected_instance_id)

            print(f"Logs Info: {log_info}")

            AllureReport.attach_text(
                log_info,
                "Runtime Manager Success Logs"
            )

            assert expected_log_info in log_info, (
                f"Expected log info "
                f"'{expected_log_info}' "
                f"not found in success logs"
            )

            print(
                f"Expected log info "
                f"'{expected_log_info}' found in logs"
            )

        # ==========================================
        # ERROR RESPONSE VALIDATION
        # ==========================================
        elif str(response_status) in ["400", "404","403"]:

            error_log_info = self.get_text(self.ERROR_LOG_MESSAGE,"Error Log Message")

            print(f"Error Logs Info: {error_log_info}")

            AllureReport.attach_text(
                error_log_info,
                "Runtime Manager Error Logs"
            )

            assert expected_log_info in error_log_info, (
                f"Expected error log info "
                f"'{expected_log_info}' "
                f"not found in error logs"
            )

            print(
                f"Expected error log info "
                f"'{expected_log_info}' found in error logs"
            )

        else:
            raise Exception(
                f"Unsupported response status: "
                f"{response_status}"
            )

        # ==========================================
        # SCREENSHOT
        # ==========================================
        screenshot_path = self.take_screenshot(
            f"runtime_logs_{response_status}"
        )

        AllureReport.attach_screenshot(
            screenshot_path,
            "Runtime Manager Logs Screenshot"
        )


    def goto_runtime_verify_post_logs_matched(self,response_status,expected_log_info):

        self.refresh_and_wait(30)
        time.sleep(5)
        self.click(self.LOGS_TAB,"Logs Tab")
        time.sleep(3)
        self.refresh_and_wait(15)
        # ==========================================
        # SUCCESS RESPONSE VALIDATION
        # ==========================================
        if str(response_status) in ["200", "202", "Accepted"]:

            log_info = self.get_logs_message(expected_log_info)
            #log_info=self.get_text(self.LOG_MESSAGE_CONTAINER,"INFO Log Message")
            print(f"Logs Info: {log_info}")

            assert expected_log_info in log_info, (
                f"Expected log info "
                f"'{expected_log_info}' "
                f"not found in success logs"
            )
            AllureReport.attach_text(
                log_info,
                "Runtime Manager Successfully received matched Logs"
            )

            print(
                f"Expected log info "
                f"'{expected_log_info}' found in logs"
            )

        # ==========================================
        # ERROR RESPONSE VALIDATION
        # ==========================================
        elif str(response_status) in ["400", "404","403"]:

            error_log_info = self.get_text(self.LOG_MESSAGE_CONTAINER,"INFO Log Message")

            print(f"Logs Info: {error_log_info}")

            AllureReport.attach_text(
                error_log_info,
                "Runtime Manager Error Logs"
            )

            assert expected_log_info in error_log_info, (
                f"Expected error log info "
                f"'{expected_log_info}' "
                f"not found in error logs"
            )

            print(
                f"Expected error log info "
                f"'{expected_log_info}' found in error logs"
            )

        else:
            raise Exception(
                f"Unsupported response status: "
                f"{response_status}"
            )

        # ==========================================
        # SCREENSHOT
        # ==========================================
        screenshot_path = self.take_screenshot(
            f"runtime_logs_{response_status}"
        )

        AllureReport.attach_screenshot(
            screenshot_path,
            "Runtime Manager Logs Screenshot"



        )

    def goto_runtime_verify_latest_logs_matched(self, response_status, expected_log_info):

        self.refresh_and_wait(30)
        time.sleep(5)
        self.click(self.LOGS_TAB, "Logs Tab")
        time.sleep(3)
        self.refresh_and_wait(15)
        time.sleep(2)
        # ==========================================
        # SUCCESS RESPONSE VALIDATION
        # ==========================================

        if str(response_status) in ["200", "202", "Accepted"]:
            #log_info = self.get_logs_message(expected_log_info)
            log_info = self.get_text(self.LOG_MESSAGE_CONTAINER, "INFO Log Message")
            print(f"Logs Info: {log_info}")

            assert expected_log_info in log_info, (
                f"Expected log info "
                f"'{expected_log_info}' "
                f"not found in success logs"
            )
            AllureReport.attach_text(
                log_info,
                "Runtime Manager Successfully received matched Logs"
            )

            print(
                f"Expected log info "
                f"'{expected_log_info}' found in logs"
            )

        # ==========================================
        # ERROR RESPONSE VALIDATION
        # ==========================================
        elif str(response_status) in ["400", "404", "403"]:

            error_log_info = self.get_text(self.LOG_MESSAGE_CONTAINER, "INFO Log Message")

            print(f"Logs Info: {error_log_info}")

            AllureReport.attach_text(
                error_log_info,
                "Runtime Manager Error Logs"
            )

            assert expected_log_info in error_log_info, (
                f"Expected error log info "
                f"'{expected_log_info}' "
                f"not found in error logs"
            )

            print(
                f"Expected error log info "
                f"'{expected_log_info}' found in error logs"
            )

        else:
            raise Exception(
                f"Unsupported response status: "
                f"{response_status}"
            )

        # ==========================================
        # SCREENSHOT
        # ==========================================
        screenshot_path = self.take_screenshot(
            f"runtime_logs_{response_status}"
        )

        AllureReport.attach_screenshot(
            screenshot_path,
            "Runtime Manager Logs Screenshot"

        )

    def goto_runtime_verify_logs_event_id_matched(self,response_status,expected_event_id):

        self.refresh_and_wait(30)
        time.sleep(5)
        self.click(self.LOGS_TAB, "Logs Tab")
        time.sleep(3)
        self.refresh_and_wait(15)
        # ==========================================
        # SUCCESS RESPONSE VALIDATION
        # ==========================================
        if str(response_status) in ["200", "202", "Accepted"]:

            log_info = self.get_logs_message(expected_event_id)

            print(f"Logs Info: {log_info}")

            AllureReport.attach_text(
                log_info,
                "Runtime Manager Success Logs"
            )

            assert expected_event_id in log_info, (
                f"Expected log info "
                f"'{expected_event_id}' "
                f"not found in success logs"
            )

            print(
                f"Expected log info "
                f"'{expected_event_id}' found in logs"
            )

        # ==========================================
        # ERROR RESPONSE VALIDATION
        # ==========================================
        elif str(response_status) in ["400", "404","403"]:

            #error_log_info = self.get_logs_alert_message(expected_event_id)

            error_log_info = self.get_text(self.LOG_SEARCH_ALERT_MESSAGE_CONTAINER,"INFO Log Message")

            print(f"Logs Info: {error_log_info}")

            AllureReport.attach_text(
                error_log_info,
                "Runtime Manager Error Logs"
            )

            assert expected_event_id in error_log_info, (
                f"Expected error log info "
                f"'{expected_event_id}' "
                f"not found in error logs"
            )

            print(
                f"Expected error log info "
                f"'{expected_event_id}' found in error logs"
            )

        else:
            raise Exception(
                f"Unsupported response status: "
                f"{response_status}"
            )

        # ==========================================
        # SCREENSHOT
        # ==========================================
        screenshot_path = self.take_screenshot(
            f"runtime_logs_{response_status}"
        )

        AllureReport.attach_screenshot(
            screenshot_path,
            "Runtime Manager Logs Screenshot"
        )


    def goto_runtime_verify_logs_instance_id_matched_Alert_message(self,response_status,expected_instance_id):

        self.refresh_and_wait(30)
        time.sleep(5)
        self.click(self.LOGS_TAB, "Logs Tab")
        time.sleep(3)
        self.refresh_and_wait(15)

        # ==========================================
        # ERROR RESPONSE VALIDATION
        # ==========================================
        if str(response_status) in ["400", "404","403"]:

            error_log_info = self.get_logs_instance_alert_message(expected_instance_id)

            print(f"Logs Info: {error_log_info}")

            AllureReport.attach_text(
                error_log_info,
                "Runtime Manager Error Logs"
            )

            assert expected_instance_id in error_log_info, (
                f"Expected error log info "
                f"'{expected_instance_id}' "
                f"not found in error logs"
            )

            print(
                f"Expected error log info "
                f"'{expected_instance_id}' found in error logs"
            )

        else:
            raise Exception(
                f"Unsupported response status: "
                f"{response_status}"
            )

        # ==========================================
        # SCREENSHOT
        # ==========================================
        screenshot_path = self.take_screenshot(
            f"runtime_logs_{response_status}"
        )

        AllureReport.attach_screenshot(
            screenshot_path,
            "Runtime Manager Logs Screenshot"
        )

    def goto_runtime_verify_logs_search_event_id_alert_message(self,response_status,expected_event_id):

        self.refresh_and_wait(30)
        time.sleep(5)
        self.click(self.LOGS_TAB, "Logs Tab")
        time.sleep(3)
        self.refresh_and_wait(15)

        if str(response_status) in ["400", "404","403"]:

            error_log_info = self.get_logs_alert_message(expected_event_id)

            print(f"Logs Info: {error_log_info}")

            AllureReport.attach_text(
                error_log_info,
                "Runtime Manager Error Logs"
            )

            assert expected_event_id in error_log_info, (
                f"Expected error log info "
                f"'{expected_event_id}' "
                f"not found in error logs"
            )

            print(
                f"Expected error log info "
                f"'{expected_event_id}' found in error logs"
            )

        else:
            raise Exception(
                f"Unsupported response status: "
                f"{response_status}"
            )

        # ==========================================
        # SCREENSHOT
        # ==========================================
        screenshot_path = self.take_screenshot(
            f"runtime_logs_{response_status}"
        )

        AllureReport.attach_screenshot(
            screenshot_path,
            "Runtime Manager Logs Screenshot"
        )


    def goto_runtime_verify_logs_invalid_msg_received(self,response_status,expected_log_info):

        self.refresh_and_wait(30)
        time.sleep(5)
        self.click(self.LOGS_TAB, "Logs Tab")
        time.sleep(3)
        self.refresh_and_wait(15)
        # ==========================================
        # SUCCESS RESPONSE VALIDATION
        # ==========================================
        if str(response_status) in ["400", "404","403"]:

            error_log_info = self.get_text(self.INVALID_INPUT_LOG_MSG,"Error Log Message")

            print(f"Error Logs Info: {error_log_info}")

            AllureReport.attach_text(
                error_log_info,
                "Runtime Manager Error Logs"
            )

            assert expected_log_info in error_log_info, (
                f"Expected error log info "
                f"'{expected_log_info}' "
                f"not found in error logs"
            )

            print(
                f"Expected error log info "
                f"'{expected_log_info}' found in error logs"
            )

        else:
            raise Exception(
                f"Unsupported response status: "
                f"{response_status}"
            )

        # ==========================================
        # SCREENSHOT
        # ==========================================
        screenshot_path = self.take_screenshot(
            f"runtime_logs_{response_status}"
        )

        AllureReport.attach_screenshot(
            screenshot_path,
            "Runtime Manager Logs Screenshot"
        )



    def get_logs_message(self,search_input):
        # Wait for logs to load and return the log messages
        self.clear_text(self.LOG_SEARCH_INPUT)
        self.enter_text(self.LOG_SEARCH_INPUT,search_input, "Log Search Input")
        self.press_enter()
        log_msg_locator = (
            By.XPATH,
            f"(//pre[contains(.,'{search_input}')])[last()]"
        )

        element = WebDriverWait(self.driver, 60).until(
            lambda driver: driver.find_element(*log_msg_locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        log_message = self.driver.execute_script(
            "return arguments[0].innerText;",
            element
        )

        print("Fetched text from Log Message Info")
        print(log_message)
        return log_message

    def get_logs_alert_message(self,search_input):
        # Wait for logs to load and return the log messages
        self.clear_text(self.LOG_SEARCH_INPUT)
        self.enter_text(self.LOG_SEARCH_INPUT,search_input, "Log Search Input")
        self.press_enter()
        time.sleep(2)
        #log_messages= self.get_text(self.INFO_ALERT_LOG_MESSAGE,"Alert Log Message Container")
        wait = WebDriverWait(self.driver, 20)

        logs = wait.until(
            lambda d: d.find_elements(
                By.XPATH,
                "//pre[contains(., 'Alert message published to alert queue')]"
            )
        )

        if not logs:
            raise Exception("No alert logs found")

        # safest option: take LAST log
        return logs[-1].text
        #return log_messages


    def get_logs_instance_alert_message(self,search_input):
        # Wait for logs to load and return the log messages
        self.clear_text(self.LOG_SEARCH_INPUT)
        self.enter_text(self.LOG_SEARCH_INPUT,search_input, "Log Search Input")
        self.press_enter()
        time.sleep(2)
        log_messages = self.get_text(self.LOG_MESSAGE_CONTAINER, "Log Message Container")
        return log_messages









