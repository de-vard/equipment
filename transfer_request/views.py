from django.db.models import Q
from rest_framework import permissions, generics
from rest_framework.throttling import UserRateThrottle

from base.views.bases import BaseTransferRequestListView
from transfer_request.models import TransferRequest
from transfer_request.permissions import IsReceiverOrReadOnly, IsActiveUser
from transfer_request.serializers import TransferRequestSerializer, CreateTransferRequestSerializer, \
    UpdateTransferRequestSerializer


class IncomingTransferRequestsView(BaseTransferRequestListView):
    """
    Представление для просмотра входящих заявок на перемещение оборудования.
    Показывает только те заявки, где текущий пользователь указан как получатель (receiver).
    """
    filter_field = 'receiver'


class PendingIncomingTransferRequestsView(BaseTransferRequestListView):
    """
    Просмотр входящих заявок на перемещение оборудования со статусом 'Ожидание'.
    """
    filter_field = 'receiver'
    status_filter = 'pending'


class OutgoingTransferRequestsView(BaseTransferRequestListView):
    """
    API endpoint для просмотра ИСХОДЯЩИХ заявок на перемещение оборудования.
    Показывает только те заявки, которые создал текущий пользователь (где он отправитель).
    """
    filter_field = 'sender'


class PendingOutgoingTransferRequestsView(BaseTransferRequestListView):
    """
    Просмотр исходящих заявок на перемещение оборудования со статусом 'Ожидание'.
    """
    filter_field = 'sender'
    status_filter = 'pending'


class TransferRequestCreateView(generics.CreateAPIView):
    """Только для создания заявок на перемещение оборудования"""
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]
    queryset = TransferRequest.objects.all()
    serializer_class = CreateTransferRequestSerializer
    throttle_classes = [UserRateThrottle]  # Ограничение запросов для пользователя

    def perform_create(self, serializer):
        """Автоматически назначает отправителя (текущего пользователя)"""
        serializer.save(sender=self.request.user)


class TransferRequestDetailView(generics.RetrieveAPIView):
    """ Детальный просмотр заявки"""
    serializer_class = TransferRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'public_id'

    def get_queryset(self):
        return TransferRequest.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )


class TransferRequestUpdateView(generics.UpdateAPIView):
    """Только для принятия или отказа от оборудования"""
    serializer_class = UpdateTransferRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsReceiverOrReadOnly]
    lookup_field = 'public_id'

    def get_queryset(self):
        return TransferRequest.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )
