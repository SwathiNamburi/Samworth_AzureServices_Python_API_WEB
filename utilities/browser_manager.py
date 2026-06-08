from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BrowserManager:

    @staticmethod
    def launch_browser(headless=False):

        options = Options()

        # Run headless only when passed from terminal
        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")

        # Browser console logs
        options.set_capability(
            "goog:loggingPrefs",
            {"browser": "ALL"}
        )

        driver = webdriver.Chrome(
            options=options
        )

        return driver

    @staticmethod
    def close_browser(driver):

        if driver:
            driver.quit()