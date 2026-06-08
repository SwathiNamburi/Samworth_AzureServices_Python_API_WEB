import os
from datetime import datetime
import time
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import (Select)
from selenium.webdriver.support.wait import WebDriverWait
from utilities.waits import Waits
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):

        self.driver = driver

    # =====================================================
    # CLICK OPERATIONS
    # =====================================================

    def click(
            self,
            locator,
            element_name
    ):

        Waits.wait_until_clickable(
            self.driver,
            locator
        ).click()

        print(
            f"Clicked on {element_name}"
        )

    def clear_text(self, locator):
        element = (
            Waits.wait_until_visible(
                self.driver,
                locator
            )
        )

        element.clear()

    def enter_text(
            self,
            locator,
            text,
            element_name
    ):

        element = (
            Waits.wait_until_visible(
                self.driver,
                locator
            )
        )

        element.clear()

        element.send_keys(text)

    def press_enter(self):
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    def get_text(
            self,
            locator,
            element_name
    ):

        retries = 3
        wait_time = 5

        for attempt in range(retries):

            try:

                text = Waits.wait_until_visible(
                    self.driver,
                    locator,
                    wait_time
                ).text.strip()

                if text:
                    print(
                        f"Fetched text from "
                        f"{element_name}"
                    )

                    return text

            except Exception as e:

                print(
                    f"Attempt {attempt + 1} failed "
                    f"for {element_name}: {e}"
                )

            time.sleep(2)

        raise Exception(
            f"Unable to fetch text from "
            f"{element_name} after {retries} retries"
        )

    def is_element_visible(
            self,
            locator,
            element_name
    ):

        visible = (
            Waits.wait_until_visible(
                self.driver,
                locator
            ).is_displayed()
        )

        print(
            f"{element_name} is visible"
        )

        return visible

    def select_by_visible_text(
            self,
            locator,
            text,
            element_name
    ):

        dropdown = Select(
            Waits.wait_until_visible(
                self.driver,
                locator
            )
        )

        dropdown.select_by_visible_text(
            text
        )

        print(
            f"Selected '{text}' "
            f"from {element_name}"
        )

    def navigate_to(self, url):

        self.driver.get(url)

        print(
            f"Navigated to URL: {url}"
        )

    def scroll_into_view(
            self,
            locator,
            element_name
    ):
        element = Waits.wait_until_visible(
            self.driver,
            locator
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

        print(
            f"Scrolled to {element_name}"
        )

        return element

    def wait_until_enabled(
            self,
            locator,
            element_name,
            timeout=30
    ):
        element = WebDriverWait(
            self.driver,
            timeout
        ).until(
            EC.element_to_be_clickable(locator)
        )

        print(
            f"{element_name} is enabled"
        )

        return element

    def wait_for_page_load(
            self,
            timeout=30
    ):
        WebDriverWait(
            self.driver,
            timeout
        ).until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        print("Page loaded successfully")



    def take_screenshot(self, screenshot_name):
        # create screenshots folder if not exists
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        # timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # full path
        screenshot_path = (
            f"{screenshot_dir}/"
            f"{screenshot_name}_{timestamp}.png"
        )

        # capture screenshot
        self.driver.save_screenshot(screenshot_path)

        print(f"Screenshot saved: {screenshot_path}")

        return screenshot_path



    def switch_to_frame(
            self,
            locator,
            frame_description="Frame"
    ):
        self.driver.switch_to.default_content()

        WebDriverWait(
            self.driver,
            30
        ).until(
            EC.frame_to_be_available_and_switch_to_it(locator)
        )

        print(f"Switched to {frame_description}")

        # ==========================================
        # REFRESH CURRENT PAGE
        # ==========================================

    def refresh_page(self):
        self.driver.refresh()

        print("Page refreshed successfully")


        # ==========================================
        # REFRESH + WAIT
        # ==========================================

    def refresh_and_wait(self, timeout):
        self.refresh_page()

        self.wait_for_page_load(timeout)

        print("Page refreshed and fully loaded")
