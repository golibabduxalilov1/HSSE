from rest_framework.permissions import BasePermission


class CanCreateReport(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class CanViewReport(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if user.is_admin():
            return True
        
        if user.is_employee():
            return obj.reporter == user or obj.assignee == user
        
        return False


class CanEditReport(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if user.is_admin():
            return True
        
        if user.is_employee():
            return obj.assignee == user
        
        return False


class CanDeleteReport(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_superadmin()