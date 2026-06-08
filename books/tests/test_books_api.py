import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from books.models import Book


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return get_user_model().objects.create_superuser(
        email="admin@test.com",
        password="testpass123",
    )


@pytest.fixture
def book():
    return Book.objects.create(
        title="Test Book",
        author="Test Author",
        cover=Book.CoverChoices.HARD,
        inventory=5,
        daily_fee="1.99",
    )


@pytest.mark.django_db
def test_list_books_allowed_for_anonymous_user(api_client, book):
    response = api_client.get("/api/books/")

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_book_allowed_for_admin(api_client, admin_user):
    api_client.force_authenticate(admin_user)

    payload = {
        "title": "New Book",
        "author": "New Author",
        "cover": Book.CoverChoices.SOFT,
        "inventory": 10,
        "daily_fee": "2.50",
    }

    response = api_client.post("/api/books/", payload)

    assert response.status_code == 201
    assert Book.objects.count() == 1


@pytest.mark.django_db
def test_create_book_forbidden_for_anonymous_user(api_client):
    payload = {
        "title": "New Book",
        "author": "New Author",
        "cover": Book.CoverChoices.SOFT,
        "inventory": 10,
        "daily_fee": "2.50",
    }

    response = api_client.post("/api/books/", payload)

    assert response.status_code in (401, 403)
