# Paylocity STE Assessment – Bug Challenge

## Overview

This repository contains an automated test suite created for the **Paylocity Software Test Engineer (STE) Bug Challenge**.

The purpose of this project is to identify, document, and demonstrate defects in both the **API** and **UI** of the sample **Benefits Dashboard** application.  
The automation focuses on validating core employee management scenarios and exposing validation and calculation issues in the system.

The test suite includes both **passing and intentionally failing tests** to clearly document existing defects.

## Tech Stack

- Python 3.9+
- Pytest – Test execution framework
- Selenium WebDriver – UI automation
- Requests – API automation
- WebDriver Manager – Automatic browser driver management
- Pytest-HTML – HTML test reporting

## Project Structure

```
paylocity-challenge/
│
├── api/
│   ├── client.py
│   └── test_employees_api.py
│
├── ui/
│   ├── pages/
│   │   ├── login_page.py
│   │   └── dashboard_page.py
│   └── tests/
│       ├── test_dashboard_ui.py
│
├── config/
│   └── settings.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.9 or higher
- Google Chrome installed
- Internet connection (tests run against a live environment)

## Installation

Clone the repository:

```bash
git clone https://github.com/EAMosqueda/Paylocity-challenge.git
cd paylocity-challenge
```

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Application URLs, credentials, and API authorization are configured in:

```
config/settings.py
```

This file includes:

- UI login URL
- Username and password
- API base URL
- Authorization token for API requests

No additional setup is required.

## Running the Tests

Run all tests (API + UI):

```bash
pytest
```

Run only API tests:

```bash
pytest api/
```

Run only UI tests:

```bash
pytest ui/
```

## Test Reports

After test execution, an HTML report is generated automatically:

```
report.html
```

Open this file in a browser to review:

- Test results
- Passed and failed tests
- Assertion messages describing detected defects

## Notes on Test Failures

Some tests are expected to fail.  
These failures represent real defects identified in the application, including:

- Duplicate employees being allowed
- Incorrect handling of dependant values (e.g., leading zeros)
- Missing validation and user feedback
- Data consistency issues between POST and GET API endpoints

Failing tests are intentionally designed to document these defects with clear assertion messages.

## Author

Edgar Mosqueda  
Software Test Engineer
