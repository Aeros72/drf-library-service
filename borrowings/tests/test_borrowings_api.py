from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        email="user@test.com",
        password="testpass123",
    )


@pytest.fixture
def book():
    return Book.objects.create(
        title="Test Book",
        author="Test Author",
        cover=Book.CoverChoices.HARD,
        inventory=3,
        daily_fee="1.99",
    )


@pytest.mark.django_db
def test_create_borrowing_decreases_book_inventory(api_client, user, book):
    api_client.force_authenticate(user)

    payload = {
        "book": book.id,
        "expected_return_date": date.today() + timedelta(days=7),
    }

    response = api_client.post("/api/borrowings/", payload)

    book.refresh_from_db()

    assert response.status_code == 201
    assert book.inventory == 2


@pytest.mark.django_db
def test_cannot_borrow_book_with_zero_inventory(api_client, user, book):
    api_client.force_authenticate(user)
    book.inventory = 0
    book.save()

    payload = {
        "book": book.id,
        "expected_return_date": date.today() + timedelta(days=7),
    }

    response = api_client.post("/api/borrowings/", payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_return_borrowing_increases_book_inventory(api_client, user, book):
    api_client.force_authenticate(user)

    borrowing = Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=date.today(),
        expected_return_date=date.today() + timedelta(days=7),
    )

    response = api_client.post(f"/api/borrowings/{borrowing.id}/return/")

    book.refresh_from_db()
    borrowing.refresh_from_db()

    assert response.status_code == 200
    assert borrowing.actual_return_date == date.today()
    assert book.inventory == 4


@pytest.mark.django_db
def test_cannot_return_borrowing_twice(api_client, user, book):
    api_client.force_authenticate(user)

    borrowing = Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=date.today(),
        expected_return_date=date.today() + timedelta(days=7),
        actual_return_date=date.today(),
    )

    response = api_client.post(f"/api/borrowings/{borrowing.id}/return/")

    assert response.status_code == 400


@pytest.mark.django_db
def test_filter_active_borrowings(api_client, user, book):
    api_client.force_authenticate(user)

    active_borrowing = Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=date.today(),
        expected_return_date=date.today() + timedelta(days=7),
    )
    Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=date.today(),
        expected_return_date=date.today() + timedelta(days=7),
        actual_return_date=date.today(),
    )

    response = api_client.get("/api/borrowings/?is_active=true")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == active_borrowing.id
