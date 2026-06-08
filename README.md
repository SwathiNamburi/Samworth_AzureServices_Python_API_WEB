# Playwright Python Automation Framework

This is a comprehensive Playwright Python automation framework with Page Object Model, utilities, API testing, and Allure reporting.

## Structure

- `tests/` - Test scripts
- `pages/` - Page Object Model classes with locators and actions
- `utils/` - Reusable utility functions
- `api/` - API client for API automation
- `testdata/` - Test data files (JSON)
- `reports/` - Allure reports and screenshots/videos
- `config.yaml` - Environment and credentials configuration
- `requirements.txt` - Python dependencies
- `conftest.py` - Pytest fixtures and browser setup

## Setup

1. Activate virtual environment: `.venv\Scripts\activate` (Windows)
2. Install dependencies: `pip install -r requirements.txt`
3. Install Playwright browsers: `playwright install`

## Running Tests

- Run all tests: `pytest`
- Run specific test with reports: `python run_tests.py tests/test_login.py`
- View Allure HTML report: Open `reports/test_login_allure/index.html` in your browser
- View HTML report: Open `reports/test_login.html` in your browser
- Run specific test: `pytest tests/test_login.py::test_valid_login`

## Features

- Page Object Model for maintainable code
- Popup and ad blocker handling
- Screenshot and video capture on failure
- API testing support
- YAML/JSON configuration
- Allure reporting for detailed test results

## Configuration

Edit `config.yaml` to change browser, URLs, credentials, etc.

## Adding New Tests

1. Create page classes in `pages/` with locators and methods
2. Add test data in `testdata/`
3. Write tests in `tests/` using page objects and Allure decorators
