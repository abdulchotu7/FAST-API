import pytest
import sys
import os
from fastapi import status

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

pytestmark = pytest.mark.main

def test_root(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success",
        "message": "Movie Booking API is running"
    }

def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK
