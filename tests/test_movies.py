from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.auth import create_access_token

client = TestClient(app)

def get_test_movie():
    return {
        "title": "Test Movie",
        "showtime": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "available_seats": 100
    }

def get_admin_token():
    return create_access_token({"sub": "admin"}, True)

def test_get_movies():
    test_movie = get_test_movie()
    test_movie["id"] = 1  
    user_token = create_access_token({"sub": "testuser"}, False)
    
    with patch('app.database.get_db') as mock_db:
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_query.all.return_value = [MagicMock(**test_movie)]
        mock_session.query.return_value = mock_query
        mock_db.return_value = mock_session
        
        response = client.get(
            "/movies",
            cookies={"access_token": user_token}
        )
        
    assert response.status_code == 200
    movies = response.json()
    assert len(movies) == 1
    assert movies[0]["title"] == test_movie["title"]

def test_create_movie_admin():
    test_movie = get_test_movie()
    admin_token = get_admin_token()
    
    with patch('app.database.get_db') as mock_db:
        mock_session = MagicMock()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh = lambda x: None
        mock_db.return_value = mock_session
        
        response = client.post(
            "/admin/movies",
            cookies={"access_token": admin_token},
            json=test_movie
        )
        
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_movie["title"]

def test_create_movie_non_admin():
    test_movie = get_test_movie()
    user_token = create_access_token({"sub": "testuser"}, False)
    
    response = client.post(
        "/admin/movies",
        cookies={"access_token": user_token},
        json=test_movie
    )
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized"
