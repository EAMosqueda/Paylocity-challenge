# UI Bug Report – Benefits Dashboard

## UI-01: UI Allows Creation of Duplicate Employees

**Type:** Functional / Data Integrity  
**Severity:** Medium  
**Priority:** Medium  

### Description
The UI allows creating multiple employees with identical information.

### Steps to Reproduce
1. Add an employee with valid data.
2. Add another employee with the same data.

### Expected Result
The system should prevent duplicates or show validation feedback.

### Actual Result
Duplicate employees are created successfully.

### Impact
Duplicate payroll and benefit entries.

---

## UI-02: No Validation Feedback for Invalid Dependants Value

**Type:** Validation / UX  
**Severity:** Medium  
**Priority:** Medium  

### Description
No validation error is shown when entering invalid dependant values.

### Steps to Reproduce
1. Click Add Employee.
2. Enter a negative value for dependants.
3. Submit the form.

### Expected Result
A clear validation error should be displayed.

### Actual Result
No visible validation feedback appears.

### Impact
Poor user experience and invalid data submission.

---

## UI-03: Login with Invalid Username Causes Application Crash (HTTP 405)

**Type:** Functional / Error Handling  
**Severity:** High 
**Priority:** High  

### Description
When entering incorrect login username, the application crashes and displays an HTTP 405 error instead of showing a proper validation message.

### Steps to Reproduce
1. Navigate to the login page.
2. Enter an invalid username and/or password.
3. Click Login.

### Expected Result
A clear and user-friendly error message should appear indicating invalid credentials.

### Actual Result
The application crashes and displays an HTTP 405 error page.

### Impact
Prevents users from understanding the issue, breaks the login flow, and exposes internal server behavior.

---

## UI-04: Missing Sorting Functionality in Employee Table

**Type:** Usability / Feature Gap  
**Severity:** Low
**Priority:** Low

### Description
The employee table does not provide any sorting functionality (e.g., by name, dependents, benefit cost), limiting usability for users managing multiple employees.

### Steps to Reproduce
1. Log in and navigate to the Benefits Dashboard.
2. Observe the employee table headers.
3. Attempt to sort by clicking on any column header.

### Expected Result
Columns should support sorting or provide UI indicators if sorting is not available.

### Actual Result
No sorting functionality is present.

### Impact
Reduced usability and difficulty managing large employee lists.

---

## UI-05: Employee Name Field Accepts Invalid Characters

**Type:** Validation / Data Integrity  
**Severity:** Medium
**Priority:** Medium

### Description
The employee name field accepts numbers, symbols, emojis, and single-character inputs without any validation.

### Steps to Reproduce
1. Click Add Employee.
2. Enter a name such as “123”, “@@@”, “😀”, or a single character.
3. Save the employee.

### Expected Result
The system should validate the name field and restrict invalid characters or overly short inputs.

### Actual Result
The UI accepts all inputs and saves the employee successfully.

### Impact
Leads to inconsistent or invalid employee records and reduces data quality.

---

## UI-06: Browser Back Navigation Breaks UI After Performing Actions

**Type:** Functional / Navigation
**Severity:** Medium
**Priority:** Medium

### Description
Using the browser’s Back button after performing actions such as adding, editing, or deleting an employee causes the UI to break and display a “Confirm Form Resubmission” message.

### Steps to Reproduce
1. Add, edit, or delete an employee.
2. Click the browser’s Back button.

### Expected Result
The UI should gracefully handle navigation or prevent form resubmission issues.

### Actual Result
The browser displays a “Confirm Form Resubmission” warning and the UI becomes unstable.

### Impact
Interrupts workflow and may confuse users unfamiliar with form resubmission behavior.

---

## UI-07: Multiple Rapid Clicks on Save Button Create Duplicate Employees

**Type:** Functional / Data Integrity 
**Severity:** High
**Priority:** High

### Description
Clicking the Save button multiple times before the table refreshes results in multiple duplicate employee entries being created.

### Steps to Reproduce
1. Click Add Employee.
2. Enter valid employee information.
3. Click the Save button repeatedly before the UI updates.

### Expected Result
The system should debounce or disable the Save button after the first click.

### Actual Result
Multiple duplicate employee records are created.

### Impact
Severe data integrity issues and potential payroll miscalculations.
