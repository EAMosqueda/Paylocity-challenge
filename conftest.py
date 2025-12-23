import pytest
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config.settings import AUTH_TOKEN


@pytest.fixture(scope="session")
def api_session():
    """
    Provides a reusable API session for all API tests.

    - Uses a persistent `requests.Session` to improve performance.
    - Automatically injects authentication and default headers.
    - Scoped at the session level to avoid unnecessary re-creation.

    Returns:
        requests.Session: Configured session with authorization headers.
    """
    session = requests.Session()
    session.headers.update({
        "Authorization": AUTH_TOKEN,
        "Content-Type": "application/json"
    })
    return session


@pytest.fixture
def driver():
    """
    Provides a Selenium WebDriver instance for UI tests.

    - Uses Google Chrome with WebDriverManager for automatic driver management.
    - Starts the browser maximized for better element visibility.
    - Ensures proper teardown by quitting the driver after each test.

    Yields:
        WebDriver: Selenium Chrome WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver

    driver.quit()
