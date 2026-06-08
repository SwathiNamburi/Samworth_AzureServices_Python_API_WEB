#!/usr/bin/env python3
"""
Utility to package the Allure HTML report and send it by email.

Usage:
  python utilities/send_allure_report.py --to recipient@example.com

By default the script looks for the report directory at:
  reports/allure-report
If not found it will try reports/latest then reports/allure-results.

Configuration:
The script reads SMTP and email settings from (in order):
  1) command-line arguments
  2) a config file (default: config/email_config.ini)
  3) environment variables (SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD,
     SMTP_USE_TLS, FROM_EMAIL, TO_EMAIL)

The config file should have an [EMAIL] section. See config/email_config.ini
for an example.
"""
import argparse
import configparser
import os
import shutil
import smtplib
import sys
import tempfile
from email.message import EmailMessage
from pathlib import Path


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "email_config.ini"


def find_report_dir(preferred=None):
    base = Path(__file__).resolve().parents[1]
    candidates = []
    if preferred:
        candidates.append(Path(preferred))
    candidates.extend([
        base / "reports" / "allure-report",
        base / "reports" / "latest",
        base / "reports" / "allure-results",
    ])

    for c in candidates:
        if c and c.exists() and c.is_dir():
            return c
    return None


def read_config(path):
    cfg = configparser.ConfigParser()
    if path and Path(path).exists():
        cfg.read(path)
    return cfg


def get_setting(cfg, name, default=None):
    # first check env
    if name in os.environ and os.environ[name].strip():
        return os.environ[name]
    # then config file
    if cfg and cfg.has_section("EMAIL") and cfg.has_option("EMAIL", name):
        return cfg.get("EMAIL", name)
    return default


def make_zip(src_dir: Path) -> Path:
    tmpdir = Path(tempfile.gettempdir())
    archive_name = tmpdir / f"allure_report_{os.getpid()}"
    archive_path = shutil.make_archive(str(archive_name), 'zip', root_dir=str(src_dir))
    return Path(archive_path)


def send_email(smtp_host, smtp_port, use_tls, username, password, from_addr, to_addrs, subject, body, attachment_path):
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs if isinstance(to_addrs, (list, tuple)) else [to_addrs])
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment_path and Path(attachment_path).exists():
        with open(attachment_path, 'rb') as f:
            data = f.read()
        msg.add_attachment(data, maintype='application', subtype='zip', filename=Path(attachment_path).name)

    smtp_port = int(smtp_port) if smtp_port else None
    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port or 587, timeout=30)
        server.ehlo()
        if use_tls and smtp_port != 465:
            server.starttls()
            server.ehlo()
        if username:
            server.login(username, password)
        server.send_message(msg)
        server.quit()
        return True, None
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Send Allure HTML report by email (zipped)")
    parser.add_argument('--config', help='Path to email config INI file', default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument('--report-dir', help='Path to Allure report directory (overrides defaults)')
    parser.add_argument('--to', help='Recipient email address(es), comma separated')
    parser.add_argument('--from', dest='from_addr', help='From email address')
    parser.add_argument('--subject', help='Email subject', default='Allure Test Report')
    parser.add_argument('--body', help='Email body text', default='Please find attached the Allure test report.')
    args = parser.parse_args()

    cfg = read_config(args.config)

    report_dir = find_report_dir(args.report_dir)
    if not report_dir:
        print('ERROR: Could not find an Allure report directory. Looked in reports/allure-report, reports/latest, reports/allure-results')
        sys.exit(2)

    print(f'Found report directory: {report_dir}')

    smtp_host = get_setting(cfg, 'SMTP_HOST')
    smtp_port = get_setting(cfg, 'SMTP_PORT', '587')
    smtp_username = get_setting(cfg, 'SMTP_USERNAME')
    smtp_password = get_setting(cfg, 'SMTP_PASSWORD')
    smtp_use_tls = get_setting(cfg, 'SMTP_USE_TLS', 'True').lower() in ('1', 'true', 'yes', 'y')

    from_addr = args.from_addr or get_setting(cfg, 'FROM_EMAIL')
    to_addrs = args.to or get_setting(cfg, 'TO_EMAIL')
    if not to_addrs:
        print('ERROR: No recipient address provided. Use --to or configure TO_EMAIL in the config or env')
        sys.exit(2)
    to_addrs = [addr.strip() for addr in to_addrs.split(',') if addr.strip()]

    if not from_addr:
        print('ERROR: No from address provided. Use --from or configure FROM_EMAIL in the config or env')
        sys.exit(2)

    print('Zipping report...')
    archive_path = make_zip(report_dir)
    print(f'Created archive: {archive_path}')

    print('Sending email...')
    ok, err = send_email(
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        use_tls=smtp_use_tls,
        username=smtp_username,
        password=smtp_password,
        from_addr=from_addr,
        to_addrs=to_addrs,
        subject=args.subject,
        body=args.body,
        attachment_path=archive_path,
    )

    if ok:
        print('Email sent successfully')
        # keep the archive for a short while; optionally delete
        # os.remove(archive_path)
        sys.exit(0)
    else:
        print(f'Failed to send email: {err}')
        sys.exit(1)


if __name__ == '__main__':
    main()

