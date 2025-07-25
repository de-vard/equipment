from rest_framework import viewsets, permissions

from user.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра пользователей (только чтение).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
