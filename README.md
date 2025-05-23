# Movie Booking API

A FastAPI-based movie ticket booking system with user authentication and admin features. This API allows users to browse movies, book tickets, and view their booking history. Administrators can add new movies to the system.

## Features

- **User Authentication**: JWT token-based authentication
- **Movie Management**: Browse available movies with showtimes and available seats
- **Ticket Booking**: Book tickets for available movies
- **Booking History**: View past bookings
- **Admin Panel**: Special endpoints for administrators to manage movies
- **API Documentation**: Interactive API documentation with Swagger UI

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL database (or change DATABASE_URL to use SQLite)

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd movie-booking-api
```

2. **Create a virtual environment**

```bash
python3 -m venv venv
```

3. **Activate the virtual environment**

- On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Set up environment variables**

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

6. **Database Setup**

The application will automatically create the necessary database tables when it starts. The admin user should already exist in your database.

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

- API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

### Using the FastAPI Documentation

1. Open http://localhost:8000/docs in your browser
2. You'll see all available endpoints with their descriptions
3. To test protected endpoints:
   - First, use the `/auth/login` endpoint to get a token
   - The API will automatically set a cookie with your authentication token
   - Now you can use other endpoints that require authentication
4. For admin-only endpoints, you need to login with an admin user

## API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user account
- `POST /auth/create-admin` - Create an admin account (requires admin_key)
- `POST /auth/login` - Login and get access token
- `POST /auth/logout` - Logout (clear cookie)
- `GET /auth/me` - Get current user info

### Movies
- `GET /movies` - View all movies (requires authentication)
- `POST /movies/{movie_id}/book` - Book tickets for a movie (requires authentication)
- `GET /movies/history` - View booking history (requires authentication)

### Admin Only
- `POST /admin/movies` - Add a new movie (requires admin privileges)

## Project Structure

```
.
├── app/                # Main application package
│   ├── __init__.py    # Package initialization
│   ├── auth.py        # Authentication logic
│   ├── config.py      # Configuration settings
│   ├── database.py    # Database setup
│   ├── main.py        # FastAPI app and routes
│   ├── models.py      # Database models
│   └── schemas.py     # Pydantic schemas
│
├── tests/             # Test package
│   ├── __init__.py    # Package initialization
│   ├── conftest.py    # Test fixtures and setup
│   ├── test_auth.py   # Authentication tests
│   ├── test_auth_mocks.py # Mocked authentication tests
│   ├── test_bookings.py # Booking tests
│   ├── test_main.py   # Main application tests
│   └── test_movies.py # Movie tests
│
├── .env               # Environment variables (not in version control)
├── .env.example       # Example environment variables
├── .gitignore         # Git ignore file
├── LICENSE            # License file
├── pyproject.toml     # Project configuration
├── pytest.ini        # Pytest configuration
└── requirements.txt   # Dependencies
```

## Running Tests

Run all tests:

```bash
python -m pytest
```

Run tests with coverage report:

```bash
python -m pytest --cov=app
```

For a more detailed coverage report:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Run specific test categories:

```bash
python -m pytest -m auth  # Run authentication tests
python -m pytest -m critical  # Run critical tests
python -m pytest -m unit  # Run unit tests with mocks
```

## Security

- All sensitive information is stored in environment variables
- Authentication is handled with JWT tokens
- CORS is configured to restrict access to specified origins
- Admin routes are protected with role-based access control
- Passwords are stored as plain text in the database

## License

This project is licensed under the MIT License - see the LICENSE file for details.
