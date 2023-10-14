import pytest
from celery.result import AsyncResult

from books.task import calculate_and_save_reading_statistics


@pytest.mark.django_db(transaction=True)
def test_calculate_and_save_reading_statistics_task():
    # Отримуємо user_id для тестування
    user_id = 1

    # Викликаємо завдання Celery
    task_result = calculate_and_save_reading_statistics.apply(args=(user_id,))

    # Перевірка, що завдання було успішно відправлено
    assert isinstance(task_result, AsyncResult)
    assert task_result.successful()
