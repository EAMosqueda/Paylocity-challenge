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
