from fastapi.testclient import TestClient
import pytest

def get_auth_headers(client, username, password):
    response = client.post(
        "/auth/login",
        json={"username": username, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_book_movie(client, test_user, test_movie):
    headers = get_auth_headers(client, "testuser", "testpass")
    response = client.post(
        f"/movies/{test_movie.id}/book",
        headers=headers,
        json={"seats": 2}
    )
    assert response.status_code == 200
    assert response.json()["seats"] == 2
    assert response.json()["user_id"] == test_user.id
    assert response.json()["movie_id"] == test_movie.id

def test_book_movie_with_insufficient_seats(client, test_user, test_movie):
    headers = get_auth_headers(client, "testuser", "testpass")
    response = client.post(
        f"/movies/{test_movie.id}/book",
        headers=headers,
        json={"seats": 101}  # More than available seats
    )
    assert response.status_code == 400
    assert "Not enough seats available" in response.json()["detail"]

def test_book_nonexistent_movie(client, test_user):
    headers = get_auth_headers(client, "testuser", "testpass")
    response = client.post(
        "/movies/999/book",  # Non-existent movie ID
        headers=headers,
        json={"seats": 1}
    )
    assert response.status_code == 404