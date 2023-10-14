from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from books.models import ReadingSession
from users.models import User


@shared_task
def calculate_and_save_reading_statistics(user_id):
    try:
        user = User.objects.get(id=user_id)

        today = timezone.now()
        last_7_days = today - timedelta(days=7)
        last_30_days = today - timedelta(days=30)

        total_reading_time_7_days = calculate_total_reading_time(
            user, last_7_days, today
        )
        total_reading_time_30_days = calculate_total_reading_time(
            user, last_30_days, today
        )

        user.total_reading_time_7_days = total_reading_time_7_days
        user.total_reading_time_30_days = total_reading_time_30_days
        user.save()
    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist.")


def calculate_total_reading_time(user, start_date, end_date):
    sessions = ReadingSession.objects.filter(
        user=user,
        start_time__gte=start_date,
        start_time__lte=end_date,
        end_time__isnull=False,
    )
    total_time = sum(session.duration_in_minutes() for session in sessions)
    return total_time
