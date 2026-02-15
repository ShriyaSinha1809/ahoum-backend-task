# Events Platform Backend

A production-ready, Dockerized backend for an Events Platform built with Django and Django REST Framework.

## Features

- **Authentication**: Email-based login, JWT authentication, OTP verification for signup.
- **RBAC**: Role-based access control for Seekers and Facilitators.
- **Events Management**: Create, update, list, and filter events.
- **Enrollments**: Seekers can enroll in events.
- **Background Tasks**: Scheduled emails for follow-ups and reminders using Celery and Redis.
- **Dockerized**: specific `Dockerfile` and `docker-compose.yml` for easy deployment.

## Prerequisites

- Docker and Docker Compose

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd ahoum-backend-task
   ```

2. **Build and start the services:**
   ```bash
   docker-compose up --build
   ```

3. **Run Migrations:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create Superuser (Optional):**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## usage

### API Endpoints

**Authentication**
- `POST /auth/signup/`: Register with email, password, and role (SEEKER or FACILITATOR).
- `POST /auth/verify-email/`: Verify email with OTP received in logs/console.
- `POST /auth/login/`: Login with email and password to get JWT tokens.
- `POST /auth/refresh/`: Refresh JWT access token.

**Events**
- `GET /api/events/`: List all events (Seekers). Filter by `location`, `language`, `search`.
- `POST /api/events/`: Create event (Facilitators only).
- `GET /api/events/{id}/`: Retrieve event details.
- `POST /api/events/{id}/enroll/`: Enroll in an event (Seekers only).
- `GET /api/events/dashboard/`: Get dashboard stats (Facilitators only).

**Enrollments**
- `GET /api/my-enrollments/`: List enrollments for the logged-in seeker.

### Testing

**Run Tests Script:**
To verify the entire flow (Auth + Events), you can run the provided scripts:

```bash
# Verify Authentication Flow
./test_auth.sh

# Verify Event Management Flow
./test_events.sh
```

**Verify Background Tasks:**
Logs can be checked to see scheduled tasks execution.
```bash
docker-compose logs celery
```
Or run the manual verification script:
```bash
docker-compose exec web python test_tasks.py
```

## Technologies

- Python 3.11
- Django 4.2+
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker
