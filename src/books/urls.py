from django.urls import include, path
from rest_framework.routers import DefaultRouter

from books.api import BookViewSet

router = DefaultRouter()
router.register("", BookViewSet)

router.register(
    r"total_reading_time_per_book",
    BookViewSet,
    basename="total_reading_time_per_book",
)
router.register(r"user_statistics", BookViewSet, basename="user_statistics")

urlpatterns = [
    path("", include(router.urls)),
]
