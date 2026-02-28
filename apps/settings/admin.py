from django.contrib import admin
from .models import *


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "address")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "branch", "status")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status")


@admin.register(RiskCategory)
class RiskCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "severity", "status")


@admin.register(ReportType)
class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type_code", "status")
