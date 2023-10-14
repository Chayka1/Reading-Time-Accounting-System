import os
import sys

import django
import pytest  # noqa
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from books.serializers import BookSerializer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"


django.setup()
User = get_user_model()


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Тестовая книга",
            author="Тестовый автор",
        )

    def test_get_book_list(self):
        url = reverse("books")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        serialized_data = BookSerializer(self.book).data
        self.assertEqual(response.data[0], serialized_data)

    def test_create_book(self):
        url = reverse("books")
        data = {
            "title": "Новая книга",
            "author": "Тестовый автор",
            "publication_year": 2022,
            "short_description": "Краткое описание",
            "full_description": "Полное описание книги",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)


class UserAPITestCase(APITestCase):
    def test_create_user(self):
        url = reverse("users")

        data = {"email": "max@email.com", "password": "12345"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что пользователь был успешно создан
        self.assertEqual(User.objects.count(), 1)

        # Проверяем, что email совпадает с ожидаемым email
        self.assertEqual(User.objects.get().email, "max@email.com")
