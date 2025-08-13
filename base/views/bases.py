from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from transfer_request.models import TransferRequest
from transfer_request.serializers import TransferRequestSerializer


class BaseTransferRequestListView(generics.ListAPIView):
    """
    Базовый класс для представлений списка заявок на перемещение оборудования.
    """
    serializer_class = TransferRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination  # Включаем пагинацию по страницам
    page_size = 10  # Количество элементов на странице (опционально)
    filter_field = None  # Поле для фильтрации (sender или receiver)
    status_filter = None  # Опциональный фильтр по статусу

    def get_queryset(self):
        queryset = TransferRequest.objects.filter(**{self.filter_field: self.request.user})
        if self.status_filter:
            queryset = queryset.filter(status=self.status_filter)
        return queryset
