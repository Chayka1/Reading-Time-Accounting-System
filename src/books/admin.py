from django.contrib import admin

from books.models import Book, ReadingSession


@admin.register(Book)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "publication_year",
        "short_description",
        "full_description",
    ]
    list_filter = ["author"]
    search_fields = [
        "title",
        "author",
        "publication_year",
    ]


@admin.register(ReadingSession)
class UserAdmin(admin.ModelAdmin):  # noqa
    readonly_fields = ["user", "book", "start_time", "end_time"]
    list_display = [
        "user",
        "book",
        "start_time",
        "end_time",
    ]
    list_filter = ["user", "book"]
    search_fields = [
        "user",
        "book",
    ]
