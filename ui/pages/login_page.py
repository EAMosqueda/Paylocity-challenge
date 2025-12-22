from selenium.webdriver.common.by import By
from config.settings import BASE_UI_URL, USERNAME, PASSWORD

class LoginPage:

    USERNAME_INPUT = (By.ID, "Username")
    PASSWORD_INPUT = (By.ID, "Password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get(BASE_UI_URL)

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
