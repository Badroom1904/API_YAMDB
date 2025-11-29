from rest_framework import permissions


class OnlyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'admin' and request.user.is_authenticated


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin' and request.user.is_authenticated
        )


class AuthorOrModeratorOrAdminOrReadOnly(
    permissions.IsAuthenticatedOrReadOnly
):

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
        )
