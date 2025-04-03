from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
from app.auth import create_access_token
from passlib.context import CryptContext

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_test_user():
    return {
        "id": 1,
        "username": "testuser",
        "password": pwd_context.hash("testpass"),
        "is_admin": False
    }

def get_test_admin():
    return {
        "id": 2,
        "username": "admin",
        "password": pwd_context.hash("adminpass"),
        "is_admin": True
    }

def test_login_success():
    test_user = get_test_user()
    
    with patch('app.auth.get_db') as mock_db:
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = MagicMock(**test_user)
        mock_session.query.return_value = mock_query
        mock_db.return_value = mock_session
        
        response = client.post(
            "/auth/login",
            data={"username": "testuser", "password": "testpass"}
        )
        
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    with patch('app.auth.get_db') as mock_db:
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session.query.return_value = mock_query
        mock_db.return_value = mock_session
        
        response = client.post(
            "/auth/login",
            data={"username": "wronguser", "password": "wrongpass"}
        )
        
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_get_current_user():
    test_user = get_test_user()
    token = create_access_token({"sub": test_user["username"]}, test_user["is_admin"])
    
    with patch('app.auth.get_db') as mock_db:
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = MagicMock(**test_user)
        mock_session.query.return_value = mock_query
        mock_db.return_value = mock_session
        
        response = client.get(
            "/auth/me",
            cookies={"access_token": token}
        )
        
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user["username"]
