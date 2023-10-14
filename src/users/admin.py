from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["groups", "password"]
    readonly_fields = [
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
        "email",
        "total_reading_time_7_days",
        "total_reading_time_30_days",
    ]
    list_filter = ["is_active", "first_name"]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "total_reading_time_7_days",
        "total_reading_time_30_days",
    ]
    search_fields = ["email", "first_name"]
