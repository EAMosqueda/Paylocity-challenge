from config.settings import BASE_API_URL


class EmployeesAPI:
    """
    EmployeesAPI

    Client wrapper for Paylocity Employees REST API.
    This class centralizes all HTTP interactions related to employee
    management and is intended to be used by API tests.

    It assumes the provided session is already configured with:
    - Base headers (Authorization, Content-Type)
    - Authentication
    - Any required middleware (logging, retries, etc.)
    """

    def __init__(self, session):
        """
        Initialize the EmployeesAPI client.

        Args:
            session: A preconfigured requests.Session instance
                     with authentication and default headers.
        """
        self.session = session

    def create_employee(self, payload):
        """
        Create a new employee.

        Args:
            payload (dict): Employee payload containing required fields
                            such as id, firstName, lastName, and dependants.

        Returns:
            requests.Response: HTTP response from the API.

        Expected behavior:
            - Status code 200 on successful creation.
            - Newly created employee should be retrievable via GET /Employees.
        """
        return self.session.post(
            f"{BASE_API_URL}/api/Employees",
            json=payload
        )

    def get_employees(self):
        """
        Retrieve all employees.

        Returns:
            requests.Response: HTTP response containing the list of employees.

        Expected behavior:
            - Status code 200.
            - Response body should contain a list of employee objects.
        """
        return self.session.get(
            f"{BASE_API_URL}/api/Employees"
        )

    def get_employee(self, employee_id):
        """
        Retrieve a single employee by ID.

        Args:
            employee_id (str): Unique identifier of the employee.

        Returns:
            requests.Response: HTTP response from the API.

        Expected behavior:
            - Status code 200 if the employee exists.
            - Status code 404 if the employee does not exist.
        """
        return self.session.get(
            f"{BASE_API_URL}/api/Employees/{employee_id}"
        )

    def update_employee(self, payload):
        """
        Update an existing employee.

        Args:
            payload (dict): Full employee payload including the employee ID
                            and updated fields.

        Returns:
            requests.Response: HTTP response from the API.

        Expected behavior:
            - Status code 200 on successful update.
            - Updated data should be reflected in subsequent GET requests.
        """
        return self.session.put(
            f"{BASE_API_URL}/api/Employees",
            json=payload
        )

    def delete_employee(self, employee_id):
        """
        Delete an employee by ID.

        Args:
            employee_id (str): Unique identifier of the employee.

        Returns:
            requests.Response: HTTP response from the API.

        Expected behavior:
            - Status code 200 on successful deletion.
            - Employee should no longer appear in GET /Employees.
        """
        return self.session.delete(
            f"{BASE_API_URL}/api/Employees/{employee_id}"
        )
