import pytest
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config.settings import AUTH_TOKEN

@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({
        "Authorization": AUTH_TOKEN,
        "Content-Type": "application/json"
    })
    return session


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()