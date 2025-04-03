import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import Base, get_db
from app.models import User, Movie, Booking
from app.auth import create_access_token

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield engine
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    user = User(
        username="testuser",
        password="testpass123",  
        is_admin=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_admin(db_session):
    admin = User(
        username="testadmin",
        password="adminpass123",  
        is_admin=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture
def test_movie(db_session):
    movie = Movie(
        title="Test Movie",
        showtime=datetime.now(timezone.utc) + timedelta(days=1),
        available_seats=100
    )
    db_session.add(movie)
    db_session.commit()
    db_session.refresh(movie)
    return movie

@pytest.fixture
def test_booking(db_session, test_user, test_movie):
    booking = Booking(
        user_id=test_user.id,
        movie_id=test_movie.id,
        seats=2
    )
    test_movie.available_seats -= booking.seats
    db_session.add(booking)
    db_session.commit()
    db_session.refresh(booking)
    return booking

@pytest.fixture
def user_token(test_user):
    return create_access_token(data={"sub": test_user.username}, user_is_admin=False)

@pytest.fixture
def admin_token(test_admin):
    return create_access_token(data={"sub": test_admin.username}, user_is_admin=True)

@pytest.fixture
def authenticated_client(client, user_token):
    """A client that is already authenticated as a regular user"""
    client.cookies.set("access_token", user_token)
    return client

@pytest.fixture
def admin_client(client, admin_token):
    """A client that is already authenticated as an admin user"""
    client.cookies.set("access_token", admin_token)
    return client

@pytest.fixture
def movie_with_low_seats(db_session):
    """Create a movie with only 5 available seats"""
    movie = Movie(
        title="Almost Sold Out Movie",
        showtime=datetime.now(timezone.utc) + timedelta(days=1),
        available_seats=5
    )
    db_session.add(movie)
    db_session.commit()
    db_session.refresh(movie)
    return movie
