import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_user(api_client):
    payload = {
        "email": "user@test.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User",
    }

    response = api_client.post("/api/users/", payload)

    assert response.status_code == 201
    assert get_user_model().objects.count() == 1
    assert response.data["email"] == payload["email"]
    assert "password" not in response.data


@pytest.mark.django_db
def test_get_jwt_token(api_client):
    user = get_user_model().objects.create_user(
        email="user@test.com",
        password="testpass123",
    )

    payload = {
        "email": user.email,
        "password": "testpass123",
    }

    response = api_client.post("/api/users/token/", payload)

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_get_user_profile(api_client):
    user = get_user_model().objects.create_user(
        email="user@test.com",
        password="testpass123",
        first_name="Test",
    )
    api_client.force_authenticate(user)

    response = api_client.get("/api/users/me/")

    assert response.status_code == 200
    assert response.data["email"] == user.email
