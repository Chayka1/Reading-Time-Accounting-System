from rest_framework import serializers

from books.models import Book, ReadingSession


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "publication_year",
            "short_description",
            "full_description",
        ]


class BookSerializerListResponse(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "publication_year",
            "short_description",
        ]


class ReadingSessionSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"])
    end_time = serializers.DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"])

    class Meta:
        model = ReadingSession
        fields = [
            "id",
            "user",
            "book",
            "start_time",
            "end_time",
        ]
