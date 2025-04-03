import pytest
import sys
import os
from unittest.mock import MagicMock, patch
from fastapi import status
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.auth import create_access_token, get_current_user, authenticate_user
from app.models import User

pytestmark = pytest.mark.auth

@pytest.mark.unit
def test_create_access_token():
    test_data = {"sub": "testuser"}
    token = create_access_token(data=test_data, user_is_admin=False)
    
    assert isinstance(token, str)
    assert len(token) > 0

@pytest.mark.unit
@patch('app.auth.jwt.decode')
def test_get_current_user_valid_token(mock_decode, db_session):
    mock_decode.return_value = {
        "sub": "testuser",
        "is_admin": False,
        "exp": (datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp()
    }
    
    user = User(username="testuser", password="testpass", is_admin=False)
    db_session.add(user)
    db_session.commit()
    
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = user
    
    result = get_current_user(access_token="fake_token", db=db_mock)
    
    assert result == user
    assert result.username == "testuser"
    assert result.is_admin is False

@pytest.mark.unit
@patch('app.auth.verify_password')
def test_authenticate_user_success(mock_verify_password, db_session):
    mock_verify_password.return_value = True
    
    user = User(username="testuser", password="hashed_password", is_admin=False)
    db_session.add(user)
    db_session.commit()
    
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = user
    
    result = authenticate_user(db_mock, "testuser", "password")
    
    assert result == user
    
    mock_verify_password.assert_called_once_with("password", "hashed_password")

@pytest.mark.unit
@patch('app.auth.verify_password')
def test_authenticate_user_wrong_password(mock_verify_password, db_session):
    mock_verify_password.return_value = False
    
    user = User(username="testuser", password="hashed_password", is_admin=False)
    db_session.add(user)
    db_session.commit()
    
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = user
    
    result = authenticate_user(db_mock, "testuser", "wrong_password")
    
    assert result is None
    
    mock_verify_password.assert_called_once_with("wrong_password", "hashed_password")

@pytest.mark.unit
def test_authenticate_user_nonexistent_user(db_session):
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = None
    
    result = authenticate_user(db_mock, "nonexistent", "password")
    
    assert result is None
