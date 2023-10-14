from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book, ReadingSession
# fmt: off
from books.serializers import (BookSerializer, BookSerializerListResponse,
                               ReadingSessionSerializer)
# fmt: off
from books.task import calculate_and_save_reading_statistics


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            calculate_and_save_reading_statistics.apply_async(args=[request.user.id], countdown=5) # noqa
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = BookSerializerListResponse(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def start_reading(self, request, pk=None):
        book = self.get_object()
        user = request.user
        active_session = ReadingSession.objects.filter(
            user=user, end_time__isnull=True
        ).first()
        if active_session:
            active_session.end_time = timezone.now()
            active_session.save()
        new_session = ReadingSession.objects.create(
            user=user, book=book, start_time=timezone.now()
        )

        serializer = ReadingSessionSerializer(new_session)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def end_reading(self, request, pk=None):
        session = ReadingSession.objects.filter(
            user=request.user, book=pk, end_time__isnull=True
        ).first()
        if session:
            session.end_time = timezone.now()
            session.save()
            serializer = ReadingSessionSerializer(session)
            return Response(serializer.data)
        else:
            return Response(
                status=404, data={"message": "No active reading session for this book."} # noqa
            )

    @action(detail=False, methods=["get"])
    def total_reading_time_per_book(self, request):
        books = self.get_queryset()
        data = []

        for book in books:
            total_reading_time = book.total_reading_time()
            data.append(
                {
                    "book_id": book.id,
                    "book_title": book.title,
                    "total_reading_time": total_reading_time,
                }
            )

        return Response(data)

    @action(detail=False, methods=["get"])
    def user_statistics(self, request, *args, **kwargs):
        user = request.user

        user_reading_sessions = ReadingSession.objects.filter(user=user)

        total_reading_time = sum(
            session.duration_in_minutes() for session in user_reading_sessions
        )

        response_data = {
            "total_books_read": len(user_reading_sessions),
            "total_reading_time": total_reading_time,
        }

        return Response(response_data)
