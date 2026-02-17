from django.contrib import admin
from .models import Branch, Department


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
  list_display=['name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
  list_display=['name']