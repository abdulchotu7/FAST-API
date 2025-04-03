# Movie Booking API

A FastAPI-based REST API for movie ticket booking system that enables users to browse movies, make bookings, and allows administrators to manage movie listings with secure authentication.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication**
  - JWT token-based authentication
  - Secure cookie handling
  - Role-based access control (Admin/User)
  - Password hashing with bcrypt

- **Movie Management**
  - List all available movies
  - Filter movies by showtime
  - Check seat availability
  - Admin-only movie creation and updates

- **Booking System**
  - Secure ticket booking
  - Seat availability checking
  - Booking history
  - Multiple seat booking support

- **Security Features**
  - Password hashing
  - JWT token encryption
  - Secure cookie handling
  - CORS support
  - Input validation

## Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **JWT** - Token-based authentication
- **SQLite** - Database (can be easily switched to PostgreSQL)
- **Uvicorn** - Lightning-fast ASGI server
- **Pytest** - Testing framework

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abdulchotu7/FAST-API.git
cd FAST-API
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./sql_app.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

2. Configure CORS in `main.py` if needed:
```python
origins = [
    "http://localhost",
    "http://localhost:8080",
]
```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload --port 8000
```

2. Create initial admin user (if needed):
```bash
python scripts/create_admin.py
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Movies
- `GET /movies` - List all movies
- `GET /movies/{movie_id}` - Get movie details
- `POST /movies/{movie_id}/book` - Book movie tickets

### Admin Only
- `POST /admin/movies` - Create new movie
- `PUT /admin/movies/{movie_id}` - Update movie
- `DELETE /admin/movies/{movie_id}` - Delete movie

## Database Schema

### User
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE,
    password VARCHAR,
    is_admin BOOLEAN
)
```

### Movie
```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title VARCHAR,
    showtime DATETIME,
    available_seats INTEGER
)
```

### Booking
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    movie_id INTEGER,
    booking_time DATETIME,
    seats INTEGER
)
```

## Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## Project Structure
```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application creation and API routes
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic models
│   ├── database.py      # Database configuration
│   └── auth.py         # Authentication logic
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_auth.py
│   ├── test_movies.py
│   └── test_bookings.py
├── scripts/
│   └── create_admin.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Abdul Rauf - [@abdulchotu7](https://github.com/abdulchotu7)

Project Link: [https://github.com/abdulchotu7/FAST-API](https://github.com/abdulchotu7/FAST-API)
