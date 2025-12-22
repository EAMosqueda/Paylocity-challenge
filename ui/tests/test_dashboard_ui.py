import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import USERNAME, PASSWORD
from ui.pages.login_page import LoginPage
from ui.pages.dashboard_page import DashboardPage


def wait_for_table_update(driver, expected_count, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "table tbody tr")) == expected_count
    )


def test_add_employee(driver):
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