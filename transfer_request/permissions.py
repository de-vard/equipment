from rest_framework import permissions


class IsReceiverOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для изменений разрешаем только получателю
        return obj.receiver == request.user

class IsActiveUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active  # Только активные пользователи