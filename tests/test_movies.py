from fastapi.testclient import TestClient
import pytest
from datetime import datetime, timedelta

def get_auth_headers(client, username, password):
    response = client.post(
        "/auth/login",
        json={"username": username, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_movie(client, test_admin):
    headers = get_auth_headers(client, "admin", "adminpass")
    response = client.post(
        "/admin/movies",
        headers=headers,
        json={
            "title": "New Movie",
            "showtime": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "available_seats": 100
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Movie"

def test_get_movies(client, test_movie):
    response = client.get("/movies")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["title"] == "Test Movie"

def test_non_admin_cannot_create_movie(client, test_user):
    headers = get_auth_headers(client, "testuser", "testpass")
    response = client.post(
        "/admin/movies",
        headers=headers,
        json={
            "title": "New Movie",
            "showtime": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "available_seats": 100
        }
    )
    assert response.status_code == 403