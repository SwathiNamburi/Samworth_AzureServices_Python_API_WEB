import time

from selenium.webdriver.support.ui import (
    WebDriverWait
)

from selenium.webdriver.support import (
    expected_conditions as EC
)


class Waits:

    @staticmethod
    def wait_until_clickable(
            driver,
            locator,
            timeout=10
    ):

        return WebDriverWait(
            driver,
            timeout
        ).until(
            EC.element_to_be_clickable(locator)
        )

    @staticmethod
    def wait_until_visible(
            driver,
            locator,
            timeout=20
    ):

        return WebDriverWait(
            driver,
            timeout
        ).until(
            EC.visibility_of_element_located(locator)
        )

    @staticmethod
    def wait_until_present(
            driver,
            locator,
            timeout=10
    ):

        return WebDriverWait(
            driver,
            timeout
        ).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_manual_input(seconds, message):
        print(message)
        time.sleep(seconds)