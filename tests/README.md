# Test Suite for Movie Booking API

This directory contains tests for the Movie Booking API application.

## Test Structure

- `conftest.py` - Contains shared fixtures and test setup
- `test_auth.py` - Tests for authentication functionality
- `test_bookings.py` - Tests for movie booking functionality
- `test_main.py` - Tests for the main application endpoints
- `test_movies.py` - Tests for movie management functionality

## Running Tests

Run all tests:
```bash
python -m pytest
```

Run tests with specific markers:
```bash
python -m pytest -m auth
python -m pytest -m critical
python -m pytest -m "auth and critical"
```

Run tests with verbose output:
```bash
python -m pytest -v
```

## Test Categories (Markers)

- `auth` - Authentication tests
- `movies` - Movie-related tests
- `bookings` - Booking-related tests
- `main` - Main application tests
- `critical` - Critical functionality tests
- `slow` - Tests that take longer to run
- `api` - Tests that interact with the API
