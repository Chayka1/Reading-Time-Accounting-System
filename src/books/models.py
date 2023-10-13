from datetime import timezone

from django.conf import settings
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    short_description = models.TextField()
    full_description = models.TextField()
    total_reading_time = models.IntegerField(null=True)

    def total_reading_time(self):  # noqa
        total_time = 0
        sessions = self.readingsession_set.all()
        for session in sessions:
            total_time += session.duration_in_minutes()
        return total_time

    class Meta:
        db_table = "books"

    def __str__(self):
        return self.title


class ReadingSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def duration_in_minutes(self):
        if self.end_time:
            duration = self.end_time - self.start_time
            return duration.total_seconds() / 60
        else:
            current_time = timezone.now()
            duration = current_time - self.start_time
            return duration.total_seconds() / 60

    class Meta:
        db_table = "sessions"

    def __str__(self) -> str:
        return f"Reading Session for {self.book.title} by {self.user.username}"
