from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage:

    ADD_EMPLOYEE_BUTTON = (By.ID, "add")
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    DEPENDENTS_INPUT = (By.ID, "dependants")
    SUBMIT_EMPLOYEE_BUTTON = (By.ID, "addEmployee")
    UPDATE_EMPLOYEE_BUTTON = (By.ID, "updateEmployee")

    EMPLOYEE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    EDIT_EMPLOYEE_BUTTON = (By.CSS_SELECTOR, "td:last-child i.fa-edit")
    DELETE_EMPLOYEE_BUTTON = (By.CSS_SELECTOR, "td:last-child i.fa-times")
    DELETE_CONFIRMATION = (By.ID, "deleteEmployee")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_add_employee(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.ADD_EMPLOYEE_BUTTON)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )
        button.click()

    def click_submit_button(self):
        submit_button = self.wait.until(
            EC.element_to_be_clickable(self.SUBMIT_EMPLOYEE_BUTTON)
        )
        submit_button.click()

    def click_update_button(self):
        update_button = self.wait.until(
            EC.element_to_be_clickable(self.UPDATE_EMPLOYEE_BUTTON)
        )
        update_button.click()

    def fill_employee_form(self, first_name, last_name, dependents):
        first_name_input = self.wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
        )
        first_name_input.clear()
        first_name_input.send_keys(first_name)

        last_name_input = self.wait.until(
            EC.visibility_of_element_located(self.LAST_NAME_INPUT)
        )
        last_name_input.clear()
        last_name_input.send_keys(last_name)

        dependents_input = self.wait.until(
            EC.visibility_of_element_located(self.DEPENDENTS_INPUT)
        )
        dependents_input.clear()
        dependents_input.send_keys(str(dependents))

    def get_employee_rows(self):
        return self.wait.until(
            EC.presence_of_all_elements_located(self.EMPLOYEE_ROWS)
        )

    def delete_first_employee(self):
        delete_button = self.wait.until(
            EC.element_to_be_clickable(self.DELETE_EMPLOYEE_BUTTON)
        )
        delete_button.click()

        delete_confirmation = self.wait.until(
            EC.element_to_be_clickable(self.DELETE_CONFIRMATION)
        )
        delete_confirmation.click()

    def ensure_employee_exists(self):
        if len(self.get_employee_rows()) == 0:
            self.click_add_employee()
            self.fill_employee_form("Jane", "Smith", 1)
            self.wait.until(lambda d: len(self.get_employee_rows()) >= 1)

    def edit_first_employee(self, first_name, last_name, dependents):
        first_row = self.get_employee_rows()[0]

        edit_button = first_row.find_element(*self.EDIT_EMPLOYEE_BUTTON)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            edit_button
        )
        edit_button.click()

        self.fill_employee_form(first_name, last_name, dependents)
        self.click_update_button()

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "table tbody tr"),
                last_name
            )
        )