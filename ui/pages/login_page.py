from selenium.webdriver.common.by import By
from config.settings import BASE_UI_URL, USERNAME, PASSWORD


class LoginPage:
    """
    Page Object Model for the Login page.

    This class encapsulates all locators and actions related to the
    authentication flow of the application UI.
    """

    # Locators
    USERNAME_INPUT = (By.ID, "Username")
    PASSWORD_INPUT = (By.ID, "Password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def __init__(self, driver):
        """
        Initializes the LoginPage with a Selenium WebDriver instance.

        Args:
            driver (WebDriver): Selenium WebDriver used to interact with the browser.
        """
        self.driver = driver

    def load(self):
        """
        Navigates to the base URL of the application.

        This method should be called before attempting to interact
        with any login elements.
        """
        self.driver.get(BASE_UI_URL)

    def login(self, username, password):
        """
        Performs login using the provided credentials.

        Args:
            username (str): Username or email to authenticate with.
            password (str): Password associated with the user.

        This method fills in the login form and submits it.
        It assumes the login page is already loaded.
        """
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
