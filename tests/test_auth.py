import pytest
import sys
import os
from fastapi import status

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.auth import verify_password

pytestmark = pytest.mark.auth

def test_password_verification():
    password = "testpass123"
    assert verify_password(password, password)
    assert not verify_password("wrongpass", password)

def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={"username": "newuser", "password": "newpass123"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "newuser"

def test_signup_duplicate_username(client, test_user):
    response = client.post(
        "/auth/signup",
        json={"username": "testuser", "password": "newpass123"}
    )
    assert response.status_code == status.HTTP_409_CONFLICT

@pytest.mark.critical
def test_login(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == status.HTTP_200_OK, f"Expected 200 OK, got {response.status_code}"

    data = response.json()
    assert "access_token" in data, "access_token not found in response"
    assert isinstance(data["access_token"], str), "access_token should be a string"
    assert len(data["access_token"]) > 20, "access_token seems too short"

    assert response.cookies.get("access_token") is not None, "access_token cookie not set"
    assert response.cookies.get("access_token") == data["access_token"], "Cookie token doesn't match response token"

@pytest.mark.parametrize("credentials,expected_status", [
    ({"username": "testuser", "password": "wrongpass"}, status.HTTP_401_UNAUTHORIZED),
    ({"username": "nonexistentuser", "password": "testpass123"}, status.HTTP_401_UNAUTHORIZED),
    ({"username": "", "password": ""}, status.HTTP_401_UNAUTHORIZED),
])
def test_login_invalid_credentials(client, credentials, expected_status):
    response = client.post(
        "/auth/login",
        data=credentials
    )
    assert response.status_code == expected_status

def test_logout(client):
    response = client.post("/auth/logout")
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" not in response.cookies

def test_get_current_user(client, user_token):
    response = client.get(
        "/auth/me",
        cookies={"access_token": user_token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testuser"
