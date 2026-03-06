from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    list_display = (
        "code",
        "title",
        "report_type",
        "branch",
        "reporter",
        "assignee",
        "status",
        "priority",
        "created_at",
    )
    list_filter = ("status", "priority", "report_type", "branch", "created_at")
    search_fields = (
        "code",
        "title",
        "description",
        "reporter__full_name",
        "assignee__full_name",
    )


@admin.register(ReportAttachment)
class ReportAttachmentAdmin(ModelAdmin):
    list_display = ("id", "report", "file_type", "file_name", "file_size", "created_at")
    list_filter = ("file_type", "created_at")


@admin.register(ReportComment)
class ReportCommentAdmin(ModelAdmin):
    list_display = ("id", "report", "user", "created_at")
    search_fields = ("comment", "user__full_name", "report__code")


@admin.register(ReportHistory)
class ReportHistoryAdmin(ModelAdmin):
    list_display = ("id", "report", "user", "action", "created_at")
    list_filter = ("action", "created_at")
