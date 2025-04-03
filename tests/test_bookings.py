from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.auth import create_access_token

client = TestClient(app)

def get_test_booking():
    return {
        "id": 1,
        "movie_id": 1,
        "user_id": 1,
        "seats": 2,
        "booking_time": datetime.utcnow()
    }

def get_test_movie():
    return {
        "id": 1,
        "title": "Test Movie",
        "showtime": datetime.utcnow(),
        "available_seats": 100
    }

def get_user_token():
    return create_access_token({"sub": "testuser"}, False)

def test_create_booking():
    test_booking = get_test_booking()
    test_movie = get_test_movie()
    user_token = get_user_token()
    
    with patch('app.database.get_db') as mock_db:
        mock_session = MagicMock()
        mock_movie_query = MagicMock()
        mock_movie_query.filter.return_value.first.return_value = MagicMock(**test_movie)
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh = lambda x: None
        mock_session.query.return_value = mock_movie_query
        mock_db.return_value = mock_session
        
        response = client.post(
            f"/movies/{test_booking['movie_id']}/book",
            cookies={"access_token": user_token},
            json={"seats": test_booking["seats"]}
        )
        
    assert response.status_code == 200
    data = response.json()
    assert data["seats"] == test_booking["seats"]

def test_booking_no_seats():
    test_movie = get_test_movie()
    test_movie["available_seats"] = 1
    user_token = get_user_token()
    
    with patch('app.database.get_db') as mock_db:
        mock_session = MagicMock()
        mock_movie_query = MagicMock()
        mock_movie_query.filter.return_value.first.return_value = MagicMock(**test_movie)
        mock_session.query.return_value = mock_movie_query
        mock_db.return_value = mock_session
        
        response = client.post(
            "/movies/1/book",
            cookies={"access_token": user_token},
            json={"seats": 2}
        )
        
    assert response.status_code == 400
    assert "Not enough seats available" in response.json()["detail"]

def test_booking_nonexistent_movie():
    user_token = get_user_token()
    
    with patch('app.database.get_db') as mock_db:
        mock_session = MagicMock()
        mock_movie_query = MagicMock()
        mock_movie_query.filter.return_value.first.return_value = None
        mock_session.query.return_value = mock_movie_query
        mock_db.return_value = mock_session
        
        response = client.post(
            "/movies/999/book",
            cookies={"access_token": user_token},
            json={"seats": 1}
        )
        
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"
