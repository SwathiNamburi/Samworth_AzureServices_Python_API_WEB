import json
import os
import allure
from datetime import datetime


class AllureReport:

    SCREENSHOT_FOLDER = "screenshots"

    @staticmethod
    def attach_screenshot(
            screenshot_path,
            screenshot_name="Screenshot"
    ):

        allure.attach.file(
            screenshot_path,
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )

    @staticmethod
    def attach_text(
            text,
            name="Text Attachment"
    ):

        allure.attach(
            str(text),
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )

    @staticmethod
    def attach_json(
            json_data,
            name="JSON Attachment"
    ):
        allure.attach(
            json.dumps(json_data, indent=4),
            name=name,
            attachment_type=allure.attachment_type.JSON
        )

    @staticmethod
    def attach_failure_screenshot(
            driver,
            test_name
    ):

        # Create screenshots folder if not exists
        os.makedirs(
            AllureReport.SCREENSHOT_FOLDER,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        screenshot_path = (
            f"{AllureReport.SCREENSHOT_FOLDER}/"
            f"{test_name}_{timestamp}.png"
        )

        # Capture screenshot
        driver.save_screenshot(screenshot_path)

        print(
            f"Failure screenshot saved at: "
            f"{screenshot_path}"
        )

        # Attach to Allure report
        allure.attach.file(
            screenshot_path,
            name=f"{test_name} Failure Screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        return screenshot_path