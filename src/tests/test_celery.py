import pytest
from celery.result import AsyncResult

from books.task import calculate_and_save_reading_statistics


@pytest.mark.django_db(transaction=True)
def test_calculate_and_save_reading_statistics_task():
    # Get the user_id for testing
    user_id = 1

    # Calling up the Celery task
    task_result = calculate_and_save_reading_statistics.apply(args=(user_id,))

    # Verify that the task was sent successfully
    assert isinstance(task_result, AsyncResult)
    assert task_result.successful()
