from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer
from transfer_request.models import TransferRequest
from transfer_request.serializers import TransferRequestSerializer


class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра оборудования (только чтение).
    Позволяет аутентифицированным пользователям:
    - просматривать список всего оборудования (если есть расширенный доступ)
    - или только оборудование, закрепленное за ними
    """
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Проверяем, есть ли у пользователя расширенный доступ
        if user.is_advanced_access:
            # Если есть - возвращаем все оборудование без фильтрации
            return Equipment.objects.all()
        # Если нет расширенного доступа - возвращаем только оборудование пользователя
        return Equipment.objects.filter(current_owner=user)


class EquipmentDetailWithHistoryView(generics.RetrieveAPIView):
    """
    Представление для получения детальной информации об оборудовании
    вместе с историей его перемещений.
    Наследуется от RetrieveAPIView - предоставляет только GET запрос для одного объекта.
    """
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Equipment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """ Переопределенный метод retrieve для добавления истории перемещений
            к стандартному ответу с информацией об оборудовании.
        """

        instance = self.get_object() # Получаем объект Equipment по ID из URL

        serializer = self.get_serializer(instance) # Сериализуем данные оборудования

        # Получаем историю перемещений
        transfer_history = TransferRequest.objects.filter(equipment=instance).order_by('-requested_at')
        history_serializer = TransferRequestSerializer(transfer_history, many=True)

        data = serializer.data # 1. Берем стандартные данные оборудования
        data['transfer_history'] = history_serializer.data # 2. Добавляем поле с историей перемещений
        return Response(data)


class UserEquipmentListView(generics.ListAPIView):
    """
        API endpoint для получения списка оборудования, закрепленного за текущим пользователем.
        Наследуется от generics.ListAPIView, что обеспечивает только GET-запрос для получения списка.
        Требует аутентификации пользователя.
    """
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Возвращаем только оборудование, где current_owner равен текущему пользователю
    def get_queryset(self):
        return Equipment.objects.filter(current_owner=self.request.user)