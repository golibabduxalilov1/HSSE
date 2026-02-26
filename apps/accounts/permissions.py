from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superadmin()


class IsAdmin(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin()


class IsEmployee(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_employee()


class IsOwnerOrAdmin(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        return obj == request.user