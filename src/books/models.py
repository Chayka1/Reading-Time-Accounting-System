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

    # A method that counts the total reading time of a book,
    # by summing up the time of all reading sessions (ReadingSession)
    # for the given book.
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

    # A method that calculates the reading duration in minutes
    # for each reading session based on the start and end times of the session.
    # If the session has not yet ended,
    # the current time is used to calculate the reading time.
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
