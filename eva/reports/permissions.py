from rest_framework import permissions


class IsEvaAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "admin_EVA" or request.user.role == "admin":
            return True
        return False


class IsAccessedForTool(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.tools in obj:
            return True
        return False
