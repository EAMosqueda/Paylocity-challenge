import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import USERNAME, PASSWORD
from ui.pages.login_page import LoginPage
from ui.pages.dashboard_page import DashboardPage


def wait_for_table_update(driver, expected_count, timeout=10):
    """
    Waits until the employees table reflects the expected number of rows.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        expected_count (int): Expected number of employee rows.
        timeout (int, optional): Maximum time to wait in seconds. Defaults to 10.

    This helper is used to synchronize UI tests after add/delete actions
    that update the employees table asynchronously.
    """
    WebDriverWait(driver, timeout).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "table tbody tr")) == expected_count
    )


def test_add_employee(driver):
    """
    Verifies that a new employee can be added successfully via the UI.

    Steps:
    1. Log into the application.
    2. Capture the initial number of employees.
    3. Add a new employee.
    4. Assert the table row count increases by one.
    """
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    login.load()
    login.login(USERNAME, PASSWORD)

    initial_count = len(dashboard.get_employee_rows())

    dashboard.click_add_employee()
    dashboard.fill_employee_form("John", "Doe", 1)
    dashboard.click_submit_button()

    wait_for_table_update(driver, initial_count + 1)

    assert len(dashboard.get_employee_rows()) == initial_count + 1


def test_edit_employee(driver):
    """
    Verifies that an existing employee can be edited via the UI.

    Steps:
    1. Log into the application.
    2. Ensure at least one employee exists.
    3. Edit the first employee.
    4. Assert updated data is reflected in the UI.
    """
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    login.load()
    login.login(USERNAME, PASSWORD)

    dashboard.ensure_employee_exists()

    dashboard.edit_first_employee(
        first_name="Jane",
        last_name="Updated",
        dependents=2
    )

    assert "Updated" in driver.page_source


def test_delete_employee(driver):
    """
    Verifies that an employee can be deleted via the UI.

    Steps:
    1. Log into the application.
    2. Ensure at least one employee exists.
    3. Delete the first employee.
    4. Assert the table row count decreases by one.
    """
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    login.load()
    login.login(USERNAME, PASSWORD)

    if len(dashboard.get_employee_rows()) == 0:
        dashboard.click_add_employee()
        dashboard.fill_employee_form("Temp", "User", 0)
        wait_for_table_update(driver, 1)

    initial_count = len(dashboard.get_employee_rows())

    dashboard.delete_first_employee()

    wait_for_table_update(driver, initial_count - 1)

    assert len(dashboard.get_employee_rows()) == initial_count - 1


@pytest.mark.xfail(reason="BUG: UI allows duplicate employees")
def test_ui_should_not_allow_duplicate_employees(driver):
    """
    Verifies that the UI prevents creating duplicate employees.

    Expected behavior:
    - The system should block or reject employees with the same
      first name, last name, and dependants.

    Current behavior:
    - The UI allows duplicate employees to be created.
    """
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    login.load()
    login.login(USERNAME, PASSWORD)

    dashboard.click_add_employee()
    dashboard.fill_employee_form("John", "Doe", 1)

    rows_after_first = len(dashboard.get_employee_rows())

    dashboard.click_add_employee()
    dashboard.fill_employee_form("John", "Doe", 1)

    WebDriverWait(driver, 5).until(
        lambda d: len(dashboard.get_employee_rows()) >= rows_after_first
    )

    assert len(dashboard.get_employee_rows()) == rows_after_first, (
        "Duplicate employee should not be allowed"
    )


@pytest.mark.xfail(reason="BUG: No validation feedback for invalid dependants")
def test_ui_invalid_dependants_should_show_error(driver):
    """
    Verifies that invalid dependant values show a validation error.

    Expected behavior:
    - The UI should display a validation error for negative dependants.

    Current behavior:
    - No visible validation feedback is shown.
    """
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    login.load()
    login.login(USERNAME, PASSWORD)

    dashboard.click_add_employee()
    dashboard.fill_employee_form("Invalid", "Deps", "-1")

    error_message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".field-validation-error, .error, .text-danger")
        )
    )

    assert error_message.is_displayed()
