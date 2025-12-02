from rest_framework import permissions


class OnlyAdmin(permissions.BasePermission):
    """Только администратор."""
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class AdminOrMeOnly(permissions.BasePermission):
    """Только админ и зарегестрированный пользователь."""
    def has_permission(self, request, view):
        if view.action == 'me':
            return request.user and request.user.is_authenticated
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет полный доступ только администраторам.
    Остальные могут только читать.
    """
    def has_permission(self, request, view):
        # Разрешаем чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для записи требуем аутентификацию и права администратора
        # Временно используем is_staff, пока нет кастомного поля is_admin
        return request.user.is_authenticated and request.user.is_staff
