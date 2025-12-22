from config.settings import BASE_API_URL

class EmployeesAPI:

    def __init__(self, session):
        self.session = session

    def create_employee(self, payload):
        return self.session.post(
            f"{BASE_API_URL}/api/Employees",
            json=payload
        )

    def get_employees(self):
        return self.session.get(
            f"{BASE_API_URL}/api/Employees"
        )

    def get_employee(self, employee_id):
        return self.session.get(
            f"{BASE_API_URL}/api/Employees/{employee_id}"
        )

    def update_employee(self, payload):
        return self.session.put(
            f"{BASE_API_URL}/api/Employees",
            json=payload
        )

    def delete_employee(self, employee_id):
        return self.session.delete(
            f"{BASE_API_URL}/api/Employees/{employee_id}"
        )
