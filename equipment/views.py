from django.http import HttpResponse
from openpyxl.workbook import Workbook
from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView

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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # Изменяем search_fields для точного поиска по серийному номеру
    search_fields = [
        '=serial_number',  # Точное совпадение
        'model',  # Частичное совпадение для остальных полей
        'type__name',
        'manufacturer__name',
        'current_owner__username',
        'inverter_number',
    ]

    # Определяем поля, по которым можно сортировать
    ordering_fields = [
        'serial_number',
        'model',
        'type__name',  # Сортировка по связанному полю name модели EquipmentType
        'manufacturer__name',  # Сортировка по связанному полю name модели Manufacturer
        'current_owner__username'  # Сортировка по username владельца
    ]
    ordering = ['serial_number']  # Сортировка по умолчанию

    def get_queryset(self):
        user = self.request.user

        queryset = Equipment.objects.all().select_related(
            'type', 'manufacturer', 'current_owner'
        )

        # Проверяем, есть ли у пользователя расширенный доступ
        if user.is_advanced_access:
            # Если есть - возвращаем все оборудование без фильтрации
            return queryset
        # Если нет расширенного доступа - возвращаем только оборудование пользователя
        return queryset.filter(current_owner=user)


class EquipmentDetailWithHistoryView(generics.RetrieveAPIView):
    """
    Представление для получения детальной информации об оборудовании
    вместе с историей его перемещений.
    Наследуется от RetrieveAPIView - предоставляет только GET запрос для одного объекта.
    """
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Equipment.objects.all()
    lookup_field = 'public_id'

    def retrieve(self, request, *args, **kwargs):
        """ Переопределенный метод retrieve для добавления истории перемещений
            к стандартному ответу с информацией об оборудовании.
        """

        instance = self.get_object()  # Получаем объект Equipment по ID из URL

        serializer = self.get_serializer(instance)  # Сериализуем данные оборудования

        # Получаем историю перемещений
        transfer_history = TransferRequest.objects.filter(equipment=instance).order_by('-requested_at')
        history_serializer = TransferRequestSerializer(transfer_history, many=True)

        data = serializer.data  # 1. Берем стандартные данные оборудования
        data['transfer_history'] = history_serializer.data  # 2. Добавляем поле с историей перемещений
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
        return Equipment.objects.filter(
            current_owner=self.request.user,
            decommissioned_equipment=False
        )


class AvailableForTransferEquipmentListView(generics.ListAPIView):
    """
    API endpoint для получения списка оборудования пользователя,
    доступного для передачи (исключает оборудование в процессе передачи и списанное)
    """
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Возвращаем только оборудование, где current_owner равен текущему пользователю
    def get_queryset(self):
        # Получаем все оборудование пользователя
        user_equipment = Equipment.objects.filter(current_owner=self.request.user, decommissioned_equipment=False)

        # Исключаем оборудование с pending transfer requests
        pending_equipment_ids = TransferRequest.objects.filter(
            equipment__in=user_equipment,
            status='pending'
        ).values_list('equipment_id', flat=True)

        return user_equipment.exclude(id__in=pending_equipment_ids)


class EquipmentExportView(APIView):
    """Класс, который возвращает эксель файл со всем оборудованием """

    def get(self, request):
        queryset = Equipment.objects.all().select_related(
            'type', 'manufacturer', 'current_owner', 'legal_entity'
        )

        # Создаем Excel файл
        wb = Workbook()
        ws = wb.active
        ws.title = "Оборудование"

        # Заголовки
        headers = [
            "Серийный номер",
            "Инвентарный номер",
            "Модель",
            "Тип техники",
            "Производитель",
            "Поставщик",
            "Списано",
            "Номер счета",
            "Текущий владелец",
            "Юридическое лицо",
        ]
        ws.append(headers)

        # Данные
        for item in queryset:
            ws.append([
                item.serial_number or '-',
                item.inverter_number or '-',
                item.model or '-',
                item.type.name if item.type else '-',
                item.manufacturer.name if item.manufacturer else '-',
                item.supplier or '-',
                'Да' if item.decommissioned_equipment else 'Нет',
                item.invoice_info or '-',
                item.current_owner.get_full_name() if item.current_owner else '-',
                item.legal_entity.name if item.legal_entity else '-',
            ])

        # Формируем ответ
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=equipment_list.xlsx'
        wb.save(response)

        return response
