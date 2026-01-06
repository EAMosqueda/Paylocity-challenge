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
