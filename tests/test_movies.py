import pytest
import sys
import os
from fastapi import status
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

pytestmark = pytest.mark.movies

@pytest.fixture
def movie_data():
    return {
        "title": "New Test Movie",
        "showtime": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        "available_seats": 100
    }

def test_get_movies_unauthorized(client):
    response = client.get("/movies")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_movies_authorized(authenticated_client, test_movie):
    response = authenticated_client.get("/movies")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    assert response.json()[0]["title"] == test_movie.title

@pytest.mark.critical
@pytest.mark.api
def test_create_movie_as_admin(admin_client, movie_data):
    response = admin_client.post(
        "/admin/movies",
        json=movie_data
    )
    assert response.status_code == status.HTTP_201_CREATED, f"Expected 201 Created, got {response.status_code}"

    movie = response.json()
    assert movie["title"] == movie_data["title"], f"Expected title {movie_data['title']}, got {movie['title']}"
    assert "id" in movie, "Movie ID not found in response"
    assert isinstance(movie["id"], int), f"Expected integer ID, got {type(movie['id'])}"
    assert movie["available_seats"] == movie_data["available_seats"], "Seat count doesn't match"

def test_create_movie_as_user(client, movie_data, user_token):
    response = client.post(
        "/admin/movies",
        json=movie_data,
        cookies={"access_token": user_token}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
