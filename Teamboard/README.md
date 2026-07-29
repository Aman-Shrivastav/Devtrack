# TeamBoard API

TeamBoard is a Django REST API for a B2B knowledge base. Companies register to receive a JWT access token and API key, search curated Q&A entries, and generate usage logs. Company administrators can view platform-wide usage statistics.

## Requirements

- Python 3.12+ (or a compatible supported Python version)
- Docker Desktop (for PostgreSQL)

## Setup

1. Create and activate a virtual environment.
2. Install packages with `pip install -r requirements.txt`.
3. Create `.env` from the following keys, using your own secrets and database credentials:

   ```env
   SECRET_KEY=replace-me
   DEBUG=True
   DB_NAME=teamboard
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. Start PostgreSQL:

   ```bash
   docker compose up -d
   ```

5. Apply migrations and seed the knowledge base:

   ```bash
   python manage.py migrate
   python manage.py seed_kb
   ```

6. Run the server:

   ```bash
   python manage.py runserver
   ```

## API endpoints

| Method | Endpoint | Access |
| --- | --- | --- |
| POST | `/api/auth/register/` | Public |
| POST | `/api/auth/login/` | Public |
| POST | `/api/kb/query/` | JWT required |
| GET | `/api/admin/usage-summary/` | JWT required; company role must be `admin` |

Send a JWT in the `Authorization` header for protected endpoints:

```text
Authorization: Bearer <access-token>
```

The `seed_kb` command is idempotent: it only creates missing sample questions. To grant an account dashboard access, change its `Company.role` to `admin` through the Django admin or Django shell.

For the final Postman admin request, log in again after making that role change and save the returned access token as the `adminAccessToken` collection variable.

## Tests

Run the API test suite with:

```bash
python manage.py test api
```

The importable Postman collection is [TeamBoard.postman_collection.json](TeamBoard.postman_collection.json).
