import pytest
import sys
import os
from fastapi import status

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

pytestmark = pytest.mark.bookings

@pytest.fixture
def booking_data():
    return {"seats": 2}

def test_book_movie_success(client, test_movie, booking_data, user_token):
    response = client.post(
        f"/movies/{test_movie.id}/book",
        json=booking_data,
        cookies={"access_token": user_token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["seats"] == booking_data["seats"]

@pytest.mark.parametrize("seats,expected_status,expected_message", [
    (101, status.HTTP_400_BAD_REQUEST, "Only 100 seats available"),  # More than available
    (0, status.HTTP_422_UNPROCESSABLE_ENTITY, "Number of seats must be positive"),  # Invalid number
    (-5, status.HTTP_422_UNPROCESSABLE_ENTITY, "Number of seats must be positive"),  # Negative number
])
def test_book_movie_with_invalid_seats(authenticated_client, test_movie, seats, expected_status, expected_message):
    response = authenticated_client.post(
        f"/movies/{test_movie.id}/book",
        json={"seats": seats}
    )
    assert response.status_code == expected_status
    if expected_message:
        assert expected_message in response.text

def test_book_nonexistent_movie(client, user_token):
    response = client.post(
        "/movies/99999/book",
        json={"seats": 1},
        cookies={"access_token": user_token}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.slow
@pytest.mark.api
def test_view_booking_history(client, test_booking, user_token):
    response = client.get(
        "/movies/history",
        cookies={"access_token": user_token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    assert response.json()[0]["seats"] == test_booking.seats
