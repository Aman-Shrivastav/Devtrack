This is the documentation about pulse notify

# PulseNotify

Flight-price alert backend built with Django REST Framework, JWT, Celery, PostgreSQL, and Redis.

## Run it

1. Copy `.env.example` to `.env` and set a secure `SECRET_KEY`.
2. Start the dependencies with `docker compose up -d`.
3. Create a virtual environment, activate it, and run `pip install -r requirements.txt`.
4. Apply migrations with `python manage.py migrate`.
5. Run these in separate terminals:
   - `python manage.py runserver`
   - `celery -A pulsenotify worker --loglevel=info`
   - `celery -A pulsenotify beat --loglevel=info`

Run tests: `python manage.py test`.

## Endpoints

- Public: `POST /api/auth/register/`, `POST /api/auth/login/`, `GET /api/flights/price/?route=DEL-BOM`
- Authenticated: `POST`/`GET /api/alerts/`, `DELETE /api/alerts/<id>/`
- Admin-only: `GET /api/admin/summary/`
