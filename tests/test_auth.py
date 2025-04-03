from fastapi.testclient import TestClient
import pytest

def test_user_signup(client):
    response = client.post(
        "/auth/signup",
        json={"username": "newuser", "password": "newpass"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"

def test_user_login(client, test_user):
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login(client):
    response = client.post(
        "/auth/login",
        json={"username": "wronguser", "password": "wrongpass"}
    )
    assert response.status_code == 401