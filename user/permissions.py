from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Allows access only to admin users."""

    message = "Only Admins are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == "admin")


class IsRegularUser(permissions.BasePermission):
    """Allows access only to regular users."""

    message = "Only Regular Users are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == "regular_user")

