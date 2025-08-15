from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from user.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
        ViewSet для просмотра всех пользователей (только чтение).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserOrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """
        ViewSet для получения пользователей которые находятся
        в той же организации, что и сам пользователь(только чтение).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            organization=self.request.user.organization,  # список пользователей которые в такой же организации
            is_work=True,  # только работающие
        ).exclude(public_id=self.request.user.public_id)
