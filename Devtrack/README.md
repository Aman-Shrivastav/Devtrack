# DevTrack

DevTrack is a simple Django backend API for tracking engineering issues.
It demonstrates core OOP concepts (abstraction, inheritance, and
polymorphism) while exposing REST-style endpoints that can be tested
with Postman.

## Features

- Create and retrieve Reporters
- Create and retrieve Issues
- Filter Issues by status
- JSON file storage (no database required)
- OOP design using abstract base classes and inheritance
- Postman-friendly API endpoints

------------------------------------------------------------------------

## Project Structure

``` text
Devtrack/
│
├── manage.py
├── reporters.json
├── issues.json
│
├── devtrack/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── __init__.py
│
└── issues/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── apps.py
    └── __init__.py
```

------------------------------------------------------------------------

## Prerequisites

- Python 3.10+
- pip
- Postman (optional for testing)

------------------------------------------------------------------------

## Setup Instructions

### 1. Clone the Repository

``` bash
git clone <repository-url>
cd Devtrack
```

### 2. Create Virtual Environment

#### Windows

``` bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

``` bash
pip install django
```

### 4. Verify Project Files

Ensure the following files exist beside manage.py:

#### reporters.json

``` json
[]
```

#### issues.json

``` json
[]
```

### 5. Run Django Checks

``` bash
python manage.py check
```

Expected:

``` text
System check identified no issues (0 silenced).
```

### 6. Start the Server

``` bash
python manage.py runserver
```

Expected:

``` text
Starting development server at http://127.0.0.1:8000/
```

------------------------------------------------------------------------

## API Endpoints

### Reporter APIs

#### Create Reporter

POST

``` text
/api/reporters/
```

Body:

``` json
{
  "id": 1,
  "name": "Reporter",
  "email": "Reporter@email.com",
  "team": "core"
}
```

#### Get All Reporters

GET

``` text
/api/reporters/
```

#### Get Reporter By ID

GET

``` text
/api/reporters/?id=1
```

------------------------------------------------------------------------

### Issue APIs

#### Create Issue

POST

``` text
/api/issues/
```

Body:

``` json
{
  "id": 1,
  "title": "Login button not working",
  "description": "Users on iOS cannot tap login",
  "status": "open",
  "priority": "critical",
  "reporter_id": 1
}
```

#### Get All Issues

GET

``` text
/api/issues/
```

#### Get Issue By ID

GET

``` text
/api/issues/?id=1
```

#### Filter Issues By Status

GET

``` text
/api/issues/?status=open
```

------------------------------------------------------------------------

## Testing with Postman

1.  Start the Django server.
2.  Open Postman.
3.  Create requests for each endpoint.
4.  For POST requests:
    - Select Body
    - Select raw
    - Select JSON
    - Paste request payload
5.  Click Send.
6.  Verify response status and JSON output.

------------------------------------------------------------------------

## Common Issues

### 404 Not Found

Check: - Server is running - URL contains trailing slash - URLs are
configured correctly

Example:

``` text
/api/reporters/
```

not

``` text
/api/reporters
```

### FileNotFoundError

Ensure:

``` text
reporters.json
issues.json
```

exist beside manage.py.

### Import Errors

Verify:

``` python
INSTALLED_APPS = [
    ...
    "issues",
]
```

in settings.py.

------------------------------------------------------------------------

## OOP Concepts Demonstrated

### Abstraction

BaseEntity is an abstract class.

### Inheritance

Reporter and Issue inherit from BaseEntity.

### Polymorphism

CriticalIssue and LowPriorityIssue override describe().

### Encapsulation

Validation logic is contained inside model classes.

------------------------------------------------------------------------

## Author

Aman Shrivastav
