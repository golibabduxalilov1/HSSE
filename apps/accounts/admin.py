from django.contrib import admin
from .models import User
from django.utils.html import format_html

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = (
        "id",
        "email",
        "role",
        "created_at",
    )
