import pytest
import yaml
from playwright.sync_api import Playwright, Browser, Page
from pathlib import Path

# Load config
config_path = Path(__file__).parent / "config.yaml"
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

@pytest.fixture(scope="session")
def browser_config():
    return config

@pytest.fixture(scope="session")
def playwright_browser(playwright: Playwright, browser_config) -> Browser:
    browser_type = browser_config.get('browser', 'chromium')
    headless = browser_config.get('headless', False)
    if browser_type == 'chromium':
        browser = playwright.chromium.launch(headless=headless)
    elif browser_type == 'firefox':
        browser = playwright.firefox.launch(headless=headless)
    elif browser_type == 'webkit':
        browser = playwright.webkit.launch(headless=headless)
    else:
        browser = playwright.chromium.launch(headless=headless)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(playwright_browser: Browser, browser_config) -> Page:
    context = playwright_browser.new_context(
        viewport={'width': 1280, 'height': 1024},  # <-- CHANGED from 720 to 1024
        record_video_dir="reports/videos/" if browser_config.get('video_on_failure') else None
    )
    page = context.new_page()
    # Handle popups and ads
    page.add_init_script("""
        // Block popups
        window.open = () => null;

        // Hide common ad elements
        const hideAds = () => {
            const ads = document.querySelectorAll('[class*="ad"], [id*="ad"], [class*="popup"], [id*="popup"]');
            ads.forEach(ad => ad.style.display = 'none');
        };
        hideAds();
        // Run periodically
        setInterval(hideAds, 1000);
    """)

    yield page
    # Screenshot on failure
    if browser_config.get('screenshot_on_failure'):
        page.screenshot(path=f"reports/screenshots/{page.url.replace('/', '_')}.png")
    context.close()
