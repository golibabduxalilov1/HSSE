from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin


@admin.register(Branch)
class BranchAdmin(ModelAdmin):
    list_display = ("id", "name", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "address")


@admin.register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ("id", "name", "branch", "status", "created_at")
    list_filter = ("status", "branch", "created_at")
    search_fields = ("name", "branch__name")


@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display = ("id", "name", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name",)


@admin.register(ReportType)
class ReportTypeAdmin(ModelAdmin):
    list_display = ("id", "name", "type_code", "status", "created_at")
    list_filter = ("status", "type_code", "created_at")
    search_fields = ("name", "type_code")


@admin.register(RiskCategory)
class RiskCategoryAdmin(ModelAdmin):
    list_display = ("id", "name", "severity", "status", "created_at")
    list_filter = ("status", "severity", "created_at")
    search_fields = ("name",)
