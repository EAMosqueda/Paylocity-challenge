import uuid
import pytest
from api.client import EmployeesAPI


def employee_payload(overrides=None):
    """
    Generate a valid employee payload for API tests.

    Args:
        overrides (dict, optional): Fields to override in the default payload.

    Returns:
        dict: Employee payload compliant with the Employees API contract.

    Notes:
        - A unique UUID is generated for both `id` and `username`
          to avoid collisions across test runs.
        - Default dependants value is set to 2.
    """
    payload = {
        "id": str(uuid.uuid4()),
        "firstName": "John",
        "lastName": "Doe",
        "username": f"user_{uuid.uuid4()}",
        "dependants": 2
    }

    if overrides:
        payload.update(overrides)

    return payload


def test_create_employee(api_session):
    """
    Verify that an employee can be created successfully.

    Expected:
        - API returns HTTP 200.
    """
    api = EmployeesAPI(api_session)
    payload = employee_payload()

    response = api.create_employee(payload)

    assert response.status_code == 200


def test_get_employees(api_session):
    """
    Verify that the Employees list endpoint returns a valid response.

    Expected:
        - HTTP 200 status code.
        - Response body is a list.
    """
    api = EmployeesAPI(api_session)

    response = api.get_employees()

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_employee(api_session):
    """
    Verify that an existing employee can be updated.

    Flow:
        1. Create an employee.
        2. Update the firstName field.
        3. Verify update request succeeds.

    Expected:
        - HTTP 200 status code on update.
    """
    api = EmployeesAPI(api_session)
    payload = employee_payload()

    api.create_employee(payload)

    payload["firstName"] = "Jane"
    response = api.update_employee(payload)

    assert response.status_code == 200


def test_delete_employee(api_session):
    """
    Verify that an employee can be deleted successfully.

    Flow:
        1. Create an employee.
        2. Delete the employee by ID.

    Expected:
        - HTTP 200 status code on deletion.
    """
    api = EmployeesAPI(api_session)
    payload = employee_payload()

    api.create_employee(payload)

    response = api.delete_employee(payload["id"])

    assert response.status_code == 200


@pytest.mark.xfail(reason="BUG: Benefits calculation and employee retrieval are inconsistent")
def test_benefits_calculation(api_session):
    """
    Validate benefits calculation for an employee.

    Expected calculation:
        - Base employee cost: 1000 / year
        - Dependants: 2 * 500 = 1000 / year
        - Total benefits cost: 2000 / year
        - Per paycheck: 2000 / 26 = 76.92

    Known issues:
        - Newly created employees are not always returned by GET /Employees.
        - Benefits fields may be missing or incorrectly calculated.
    """
    api = EmployeesAPI(api_session)
    payload = employee_payload({"dependants": 2})

    create_response = api.create_employee(payload)
    assert create_response.status_code == 200

    employees = api.get_employees().json()

    employee = next(
        (e for e in employees if e.get("id") == payload["id"]),
        None
    )

    assert employee is not None, (
        "BUG: Employee created via POST is not returned by GET /Employees"
    )

    assert employee["benefitsCost"] > 0, (
        "BUG: benefitsCost is missing or zero"
    )

    assert employee["net"] < employee["gross"], (
        "BUG: net pay does not reflect benefit deductions"
    )


@pytest.mark.xfail(reason="BUG: API allows invalid dependants values")
def test_api_dependants_leading_zero_parsed_incorrectly(api_session):
    """
    Validate handling of invalid dependants input.

    Scenario:
        - Dependants value is provided as a string with leading zeros ('02').

    Expected:
        - API should reject the value OR parse it as integer 2.

    Actual:
        - API accepts the value and parses it incorrectly as 0.
    """
    api = EmployeesAPI(api_session)

    payload = {
        "id": str(uuid.uuid4()),
        "firstName": "Zero",
        "lastName": "Test",
        "username": f"zero_{uuid.uuid4()}",
        "dependants": "02"  # Invalid type, but accepted
    }

    response = api.create_employee(payload)
    assert response.status_code == 200

    employees = api.get_employees().json()
    employee = next(e for e in employees if e["id"] == payload["id"])

    assert employee["dependants"] == 0, (
        "BUG: Dependants value '02' is incorrectly parsed as 0 instead of 2 or rejected"
    )
