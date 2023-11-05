import random
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book, ReadingSession
from books.serializers import BookSerializer
# fmt: off
from books.task import (calculate_and_save_reading_statistics,
                        calculate_total_reading_time)

# fmt: off

User = get_user_model()


@pytest.fixture
def api_client():
    client = APIClient()
    email = "testuser{}@example.com".format(random.randint(1, 10000))
    user = User.objects.create_user(email=email, password="testpassword")
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def create_book():
    def _create_book(
        title="Test Book",
        author="Test Author",
        publication_year=2022,
        short_description="Short description",
        full_description="Full description",
    ):
        return Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year,
            short_description=short_description,
            full_description=full_description,
        )

    return _create_book


@pytest.fixture
def create_user():
    def _create_user(email, password):
        return User.objects.create_user(email=email, password=password)

    return _create_user


@pytest.fixture
def create_reading_session():
    def _create_reading_session(user, book, start_time=None, end_time=None):
        end_time = start_time
        return ReadingSession.objects.create(
            user=user, book=book, start_time=start_time, end_time=end_time
        )

    return _create_reading_session


@pytest.mark.django_db
def test_create_book(api_client):
    url = reverse("book-list")
    data = {
        "title": "Test Book",
        "author": "Test Author",
        "publication_year": 2022,
        "short_description": "Short description",
        "full_description": "Full description",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.count() == 1
    assert Book.objects.get().title == "Test Book"


@pytest.mark.django_db
def test_retrieve_book(api_client, create_book):
    book = create_book("Test Book", "Test Author", 2022)
    url = reverse("book-detail", kwargs={"pk": book.pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == BookSerializer(book).data


@pytest.mark.django_db
def test_list_books(api_client, create_book):
    create_book("Book 1", "Author 1", 2022)
    create_book("Book 2", "Author 2", 2022)
    url = reverse("book-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["title"] == "Book 1"
    assert response.data[1]["title"] == "Book 2"


@pytest.mark.django_db
def test_reading_sessions(api_client, create_book):
    book = create_book("Test Book", "Test Author", 2022, "Short", "Full")
    url_start = reverse("book-start-reading", kwargs={"pk": book.pk})
    response_start = api_client.post(url_start)

    assert response_start.status_code == status.HTTP_200_OK
    assert ReadingSession.objects.count() == 1

    url_end = reverse("book-end-reading", kwargs={"pk": book.pk})
    response_end = api_client.post(url_end)

    assert response_end.status_code == status.HTTP_200_OK
    assert ReadingSession.objects.count() == 1
    assert ReadingSession.objects.get().end_time is not None


@pytest.mark.django_db
def test_reading_statistics(api_client, create_book, create_reading_session):
    book1 = create_book("Book 1", "Author 1", 2022, "Short", "Full")
    book2 = create_book("Book 2", "Author 2", 2022, "Short", "Full") # noqa
    email = "testuser{}@example.com".format(random.randint(1, 10000))
    user = User.objects.create(email=email)
    create_reading_session(user, book1, start_time=timezone.now())
    url_total_reading_time = reverse("book-total-reading-time-per-book")
    response_total_reading_time = api_client.get(url_total_reading_time)

    assert response_total_reading_time.status_code == status.HTTP_200_OK
    assert len(response_total_reading_time.data) == 2
    assert response_total_reading_time.data[0]["book_id"] == 1
    assert response_total_reading_time.data[0]["total_reading_time"] == 0

    url_user_statistics = reverse("book-user-statistics")
    response_user_statistics = api_client.get(url_user_statistics)

    assert response_user_statistics.status_code == status.HTTP_200_OK
    assert response_user_statistics.data["total_books_read"] == 0
    assert response_user_statistics.data["total_reading_time"] == 0


@pytest.mark.django_db
def test_celery_tasks(create_user, create_book, create_reading_session):
    user = create_user(email="testuser@email.com", password="password")
    book = create_book("Book 1", "Author 1", 2022, "Short", "Full")
    start_time = timezone.now() - timedelta(days=7)
    end_time = timezone.now()
    create_reading_session(user, book, start_time, end_time)

    calculate_and_save_reading_statistics.apply_async(args=[user.id])
    user.refresh_from_db()

    assert user.total_reading_time_7_days is not None
    assert user.total_reading_time_30_days is not None

    calculated_7_days = calculate_total_reading_time(user, start_time, end_time) # noqa
    calculated_30_days = calculate_total_reading_time(
        user, start_time - timedelta(days=23), end_time
    )
    assert user.total_reading_time_7_days == calculated_7_days
    assert user.total_reading_time_30_days == calculated_30_days
