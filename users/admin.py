from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("email",)

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": ()
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "email",
                )
            },
        ),
    )
