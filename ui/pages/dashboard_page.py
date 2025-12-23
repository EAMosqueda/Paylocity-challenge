from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage:
    """
    Page Object representing the Employee Dashboard screen.

    Responsibilities:
        - Interact with employee table (add, edit, delete).
        - Encapsulate all UI locators and behaviors related to employees.
        - Provide high-level actions used by UI tests.

    This class follows the Page Object Model (POM) pattern.
    """

    # ─────────────────────────────
    # Locators
    # ─────────────────────────────

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
        """
        Initialize the DashboardPage.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ─────────────────────────────
    # Actions
    # ─────────────────────────────

    def click_add_employee(self):
        """
        Click the 'Add Employee' button.

        Scrolls into view to avoid click interception issues.
        """
        button = self.wait.until(
            EC.element_to_be_clickable(self.ADD_EMPLOYEE_BUTTON)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )
        button.click()

    def click_submit_button(self):
        """
        Click the 'Add Employee' submit button.
        Used when creating a new employee.
        """
        submit_button = self.wait.until(
            EC.element_to_be_clickable(self.SUBMIT_EMPLOYEE_BUTTON)
        )
        submit_button.click()

    def click_update_button(self):
        """
        Click the 'Update Employee' button.
        Used when editing an existing employee.
        """
        update_button = self.wait.until(
            EC.element_to_be_clickable(self.UPDATE_EMPLOYEE_BUTTON)
        )
        update_button.click()

    def fill_employee_form(self, first_name, last_name, dependents):
        """
        Fill the employee form fields.

        Args:
            first_name (str): Employee first name.
            last_name (str): Employee last name.
            dependents (int | str): Number of dependents.
        """
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
        """
        Retrieve all employee rows from the table.

        Returns:
            list[WebElement]: List of table row elements.
        """
        return self.wait.until(
            EC.presence_of_all_elements_located(self.EMPLOYEE_ROWS)
        )

    def delete_first_employee(self):
        """
        Delete the first employee in the table.

        Flow:
            1. Click delete icon.
            2. Confirm deletion.
        """
        delete_button = self.wait.until(
            EC.element_to_be_clickable(self.DELETE_EMPLOYEE_BUTTON)
        )
        delete_button.click()

        delete_confirmation = self.wait.until(
            EC.element_to_be_clickable(self.DELETE_CONFIRMATION)
        )
        delete_confirmation.click()

    def ensure_employee_exists(self):
        """
        Ensure that at least one employee exists in the table.

        If the table is empty, a default employee is created.
        Useful to stabilize edit/delete tests.
        """
        if len(self.get_employee_rows()) == 0:
            self.click_add_employee()
            self.fill_employee_form("Jane", "Smith", 1)
            self.click_submit_button()

            self.wait.until(
                lambda d: len(self.get_employee_rows()) >= 1
            )

    def edit_first_employee(self, first_name, last_name, dependents):
        """
        Edit the first employee in the table.

        Flow:
            1. Click edit icon on first row.
            2. Update form fields.
            3. Click update button.
            4. Wait until table reflects updated data.

        Args:
            first_name (str): Updated first name.
            last_name (str): Updated last name.
            dependents (int | str): Updated dependents count.
        """
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
