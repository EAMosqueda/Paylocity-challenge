import uuid
import pytest
from api.client import EmployeesAPI

def employee_payload(overrides=None):
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
    api = EmployeesAPI(api_session)
    payload = employee_payload()

    response = api.create_employee(payload)

    assert response.status_code == 200


def test_get_employees(api_session):
    api = EmployeesAPI(api_session)

    response = api.get_employees()

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_employee(api_session):
    api = EmployeesAPI(api_session)
    payload = employee_payload()

    api.create_employee(payload)

    payload["firstName"] = "Jane"
    response = api.update_employee(payload)

    assert response.status_code == 200


def test_delete_employee(api_session):
    api = EmployeesAPI(api_session)
    payload = employee_payload()

    api.create_employee(payload)

    response = api.delete_employee(payload["id"])
    assert response.status_code == 200

@pytest.mark.xfail(reason="BUG: Benefits calculation and employee retrieval are inconsistent")
def test_benefits_calculation(api_session):
    """
    BUG: Newly created employee is not always returned by GET /Employees
    or benefits calculations are incorrect.

    Expected:
    Employee cost = 1000/year
    Dependents = 2 * 500 = 1000/year
    Total = 2000/year
    Per paycheck = 2000 / 26 = 76.92
    """
    from api.client import EmployeesAPI

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
    BUG: Dependants with leading zeros (e.g. '02') are parsed as 0
    """
    from api.client import EmployeesAPI
    import uuid

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
