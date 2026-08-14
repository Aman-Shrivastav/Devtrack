# CollabDocs Backend API

## Setup Instructions

1. **Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   ```bash
   cp .env.example .env
   # Update .env with your DB credentials
   ```

4. **Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Server:**
   ```bash
   python manage.py runserver
   ```
