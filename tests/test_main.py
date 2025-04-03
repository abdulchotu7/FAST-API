from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from app.models import User
from sqlalchemy.orm import Session
import pytest

client = TestClient(app)

def create_admin_user(db: Session):
    admin_user = User(username="admin", password="adminpass", is_admin=True)
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    return admin_user

def get_admin_token():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "adminpass"}
    )
    return response.json()["access_token"]

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    create_admin_user(db)
    yield
    Base.metadata.drop_all(bind=engine)

def test_admin_login():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "adminpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_admin_access():
    token = get_admin_token()
    response = client.post(
        "/admin/movies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Movie",
            "showtime": "2023-07-20T10:00:00",
            "available_seats": 100
        }
    )
    assert response.status_code == 200

def test_regular_user_no_admin_access():
    # Create regular user
    client.post(
        "/auth/signup",
        json={"username": "regular_user", "password": "userpass"}
    )
    
    # Login as regular user
    response = client.post(
        "/auth/login",
        json={"username": "regular_user", "password": "userpass"}
    )
    token = response.json()["access_token"]
    
    # Try to access admin endpoint
    response = client.post(
        "/admin/movies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Movie",
            "showtime": "2023-07-20T10:00:00",
            "available_seats": 100
        }
    )
    assert response.status_code == 403
