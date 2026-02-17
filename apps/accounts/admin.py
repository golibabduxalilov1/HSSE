from django.contrib import admin
from .models import User
from django.utils.html import format_html

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = (
        "id",
        "avatar_preview",
        "email",
        "full_name",
        "role",
        "department",
        "branch",
        "is_active",
        "created_at",
    )
  list_filter=['gender', 'role', 'is_active', 'branch', 'department', 'created_at']
  search_fields=['email', 'first_name' 'last_name', 'phone']

  ordering = ('-created_at',)
  readonly_fields=('created_at', 'updated_at', 'avatar_preview')
  list_per_page = 25

  fieldsets = (
    ("Login ma'lumotlari", {
      'fields': ('email', 'password')
    }),
    ("Shaxsiy ma'lumotlar", {
      'fields': (
        'first_name',
        'last_name',
        'phone',
        'birth_date',
        'gender',
        'avatar',
        'avatar_preview',
      )
    }),
    ('Ruxsatkar', {
      'fields': (
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
        'user_permissions'
      )
    }),
    ('System', {
      'fields': ('created_at', 'updated_at'),
    }),
  )
  add_fields = (
    (None, {
      'classes': ('wide',),
      'fields': (
        'email',
        'first_name',
        'last_name',
        'password1',
        'password2',
        'role',
        'is_active',
        'is_staff',
      ),
    }),
  )

  def avatar_preview(self, obj):
    if obj.avatar:
      return format_html(
        '<img src="{}" width="40" height="40" style="border-radius:50%;" />',
        obj.avatar.url
        )
    return "-"

  avatar_preview.short_description = "Avatar"