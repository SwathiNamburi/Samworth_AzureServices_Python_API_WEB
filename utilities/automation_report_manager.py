import os
import shutil
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class AutomationReportManager:

    @staticmethod
    def generate_allure_report():

        history_source = (
            "allure-report/history"
        )

        history_destination = (
            "allure-results/history"
        )

        # Maintain report history
        if os.path.exists(history_source):

            if os.path.exists(
                    history_destination
            ):

                shutil.rmtree(
                    history_destination
                )

            shutil.copytree(
                history_source,
                history_destination
            )

        # Generate report
        os.system(
            "allure generate "
            "allure-results "
            "-o allure-report --clean"
        )

        print(
            "Allure Report Generated"
        )

    @staticmethod
    def open_allure_report():

        os.system(
            "allure open allure-report"
        )

    @staticmethod
    def zip_allure_report():

        os.system(
            "powershell Compress-Archive "
            "allure-report "
            "allure-report.zip -Force"
        )

        print(
            "Allure Report Zipped"
        )

    @staticmethod
    def send_email_report(
            sender_email,
            sender_password,
            receiver_email
    ):

        AutomationReportManager.zip_allure_report()

        subject = (
            "Automation Execution Report"
        )

        body = (
            "Please find attached "
            "Allure HTML Report."
        )

        msg = MIMEMultipart()

        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(
            MIMEText(body, "plain")
        )

        report_zip = (
            "allure-report.zip"
        )

        attachment = open(
            report_zip,
            "rb"
        )

        part = MIMEBase(
            "application",
            "octet-stream"
        )

        part.set_payload(
            attachment.read()
        )

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; "
            f"filename={report_zip}"
        )

        msg.attach(part)

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.sendmail(
            sender_email,
            receiver_email,
            msg.as_string()
        )

        server.quit()

        print(
            "Email sent successfully"
        )