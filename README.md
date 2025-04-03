# Movie Booking API

A FastAPI-based movie ticket booking system with user authentication and admin features. This API allows users to browse movies, book tickets, and view their booking history. Administrators can add new movies to the system.

## Features

- **User Authentication**: Secure JWT token-based authentication
- **Movie Management**: Browse available movies with showtimes and available seats
- **Ticket Booking**: Book tickets for available movies
- **Booking History**: View past bookings
- **Admin Panel**: Special endpoints for administrators to manage movies
- **API Documentation**: Interactive API documentation with Swagger UI

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd movie-booking-api
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

- On Windows:
```bash
venv\Scripts\activate
```

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

Edit the `.env` file to set your own values, especially the `SECRET_KEY` and `ADMIN_PASSWORD`.

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

- API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user account
- `POST /auth/login` - Login and get access token
- `POST /auth/logout` - Logout (clear cookie)
- `GET /auth/me` - Get current user info

### Movies
- `GET /movies` - View all movies
- `POST /movies/{movie_id}/book` - Book tickets for a movie
- `GET /movies/history` - View booking history

### Admin Only
- `POST /admin/movies` - Add a new movie

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

Run specific test categories:

```bash
python -m pytest -m auth  # Run authentication tests
python -m pytest -m critical  # Run critical tests
```

## Security

- All sensitive information is stored in environment variables
- Passwords are hashed using bcrypt
- Authentication is handled with JWT tokens
- CORS is configured to restrict access to specified origins

## License

This project is licensed under the MIT License - see the LICENSE file for details.
