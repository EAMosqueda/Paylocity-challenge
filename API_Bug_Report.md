# API Bug Report – Benefits Dashboard

## API-01: Newly Created Employees Are Not Always Returned by GET /Employees

**Type:** Functional / Data Consistency  
**Severity:** High  
**Priority:** High  

### Description
Employees created via POST /Employees are intermittently missing from the GET /Employees response.

### Steps to Reproduce
1. Send POST /Employees with a valid payload.
2. Verify HTTP 200 response.
3. Call GET /Employees.
4. Search for the created employee by ID.

### Expected Result
The newly created employee should always be returned by GET /Employees.

### Actual Result
The employee is sometimes missing from the response.

### Impact
Breaks data consistency, benefit calculations, and downstream workflows.

---

## API-02: Benefits Cost Fields Are Missing or Incorrectly Calculated

**Type:** Business Logic  
**Severity:** High  
**Priority:** High  

### Description
Benefit-related fields are missing, zero, or incorrectly calculated.

### Expected Calculation
- Employee: $1000 / year  
- Dependants: $500 each / year  
- Paychecks: 26  

### Actual Result
Returned values do not match expected calculations and net pay does not always reflect deductions.

### Impact
Incorrect payroll previews and core business functionality failure.

---

## API-03: Invalid Dependants Value With Leading Zeros Is Parsed Incorrectly

**Type:** Validation  
**Severity:** Medium  
**Priority:** Medium  

### Description
Dependants value provided as a string with leading zeros ("02") is accepted and parsed as 0.

### Steps to Reproduce
1. Create employee with dependants = "02".
2. Retrieve employee via GET /Employees.

### Expected Result
Value should be rejected or parsed as integer 2.

### Actual Result
Value is stored as 0.

### Impact
Silent data corruption and incorrect benefit calculations.

---

## API-04: API Allows Creation of Duplicate Employees

**Type:** Validation / Data Integrity  
**Severity:** High  
**Priority:** High

### Description
The API accepts multiple POST /Employees requests containing identical employee data, resulting in duplicate employee records. There is no backend validation to prevent duplicates.

### Steps to Reproduce
1. Send a POST /Employees request with valid employee data.
2. Send the same POST request again with identical data.
3. Call GET /Employees.
4. Observe that both records appear in the response.

### Expected Result
The API should reject duplicate employee creation with a validation error (e.g., 400 Bad Request or 409 Conflict).

### Actual Result
The API creates multiple identical employee entries without any validation feedback.

### Impact
Severe data integrity issues, incorrect payroll calculations, and potential financial inconsistencies.

---

## API-05: API Does Not Prevent Multiple Rapid Submissions (No Idempotency / Race Condition)

**Type:** Functional / Data Integrity  
**Severity:** High  
**Priority:** High

### Description
When multiple identical POST /Employees requests are sent in rapid succession (e.g., due to repeated UI clicks), the API processes all of them independently, creating duplicate employee records. The API does not implement idempotency or request throttling.

### Steps to Reproduce
1. Send multiple identical POST /Employees requests quickly (e.g., 2–5 requests within milliseconds).
2. Call GET /Employees.
3. - Observe that multiple duplicate employees were created.

### Expected Result
The API should prevent duplicate submissions by enforcing idempotency, rejecting repeated requests, or temporarily locking the resource.

### Actual Result
All requests are processed, resulting in multiple duplicate employee entries.

### Impact
Critical data duplication, inconsistent payroll calculations, and potential financial errors.
