# University Event Management System

This project is a backend application for managing university events, including user registrations, event management, and venue handling. It is built using FastAPI and follows a modular architecture.

## Project Structure

```
backend
├── src
│   ├── main.py
│   ├── config
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints
│   │           ├── __init__.py
│   │           ├── events.py
│   │           ├── users.py
│   │           ├── registrations.py
│   │           └── venues.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── exceptions.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── event.py
│   │   ├── user.py
│   │   ├── registration.py
│   │   └── venue.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── event.py
│   │   ├── user.py
│   │   ├── registration.py
│   │   └── venue.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── event_service.py
│   │   ├── user_service.py
│   │   ├── registration_service.py
│   │   └── venue_service.py
│   ├── repositories
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── event_repository.py
│   │   ├── user_repository.py
│   │   ├── registration_repository.py
│   │   └── venue_repository.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   ├── middleware
│   │   ├── __init__.py
│   │   └── error_handler.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_events.py
│   ├── test_users.py
│   ├── test_registrations.py
│   └── test_venues.py
├── alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── .gitkeep
├── alembic.ini
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd backend
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy `.env.example` to `.env` and fill in the required values.

5. **Run the application:**
   ```
   uvicorn src.main:app --reload
   ```

## Features

- User registration and management
- Event creation and management
- Venue management
- QR code generation for registrations
- Email notifications for users

## Testing

To run the tests, use:
```
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.