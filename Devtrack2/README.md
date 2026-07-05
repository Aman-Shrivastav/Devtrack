# 🎟️ EventHub

A RESTful backend API for a simplified event ticketing platform built
using **Django** and **Django REST Framework**.

## Features

-   Create, retrieve, update, and delete events
-   Reserve seats for an event
-   Prevent overbooking
-   Cancel reservations and restore seats automatically
-   Filter events by status
-   Filter events by venue
-   Filter reservations by event
-   Request logging middleware

## Tech Stack

-   Python
-   Django
-   Django REST Framework
-   SQLite

## Installation

``` bash
git clone https://github.com/<your-username>/eventhub.git
cd eventhub
python -m venv venv
```

Activate the virtual environment (Windows):

``` bash
venv\Scripts\activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run migrations:

``` bash
python manage.py migrate
```

(Optional) Create an admin user:

``` bash
python manage.py createsuperuser
```

Start the development server:

``` bash
python manage.py runserver
```

API Base URL:

    http://127.0.0.1:8000/api/

## API Endpoints

### Events

-   `GET /api/events/` --- List all events
-   `POST /api/events/` --- Create an event
-   `GET /api/events/{id}/` --- Retrieve an event
-   `PUT /api/events/{id}/` --- Update an event
-   `DELETE /api/events/{id}/` --- Delete an event

Filters:

-   `GET /api/events/?status=upcoming`
-   `GET /api/events/?venue=Bangalore`

### Reservations

-   `GET /api/reservations/`
-   `POST /api/reservations/`
-   `GET /api/reservations/{id}/`
-   `PUT /api/reservations/{id}/`
-   `DELETE /api/reservations/{id}/`
-   `POST /api/reservations/{id}/cancel/`

Filter:

-   `GET /api/reservations/?event_id=1`

## Sample Requests

### Create Event

``` json
{
  "title": "PyCon India 2025",
  "venue": "NIMHANS Convention Centre, Bangalore",
  "date": "2025-09-20",
  "total_seats": 500,
  "available_seats": 500,
  "status": "upcoming"
}
```

### Create Reservation

``` json
{
  "event": 1,
  "attendee_name": "Aman Shrivastava",
  "attendee_email": "aman@example.com",
  "seats_reserved": 2
}
```

## Validation

-   `available_seats` cannot exceed `total_seats`.
-   Reservations require at least one seat.
-   Reservations are allowed only for upcoming or ongoing events.
-   Overbooking returns `400 Bad Request`.

## Middleware

The project includes a custom `RequestLoggingMiddleware` that logs:

-   HTTP method
-   Request path
-   Response status
-   Execution time

## Design Decision

The reservation logic updates the event's available seats inside the
serializer's `create()` method before creating the reservation. This
keeps seat deduction and reservation creation together in one place. In
a production system, `transaction.atomic()` would be used to handle
concurrent reservations safely.

## Testing Checklist

-   Create an event
-   List events
-   Filter events
-   Create reservation
-   Prevent overbooking
-   Cancel reservation
-   Restore seats
-   Filter reservations
-   Verify middleware logging

## Author

**Aman Shrivastav**
