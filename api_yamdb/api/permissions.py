from rest_framework import permissions
from users.models import ROLE_ADMIN


class OnlyAdmin(permissions.BasePermission):
    """Access restricted to admin users."""
    def has_permission(self, request, view):
        return request.user.role == ROLE_ADMIN or request.user.is_superuser


class AdminOrMeOnly(permissions.BasePermission):
    """Allows access to /me for authenticated users and others for admins."""
    def has_permission(self, request, view):
        if view.action == 'me':
            return request.user.is_authenticated
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Full access for admin, read-only for others."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Write access for authors, moderators, admins; read access for all."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
