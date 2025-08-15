from django.http import HttpResponse
from openpyxl.workbook import Workbook
from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer
from transfer_request.models import TransferRequest
from transfer_request.serializers import TransferRequestSerializer

class EquipmentListView(generics.ListAPIView):
    """
    API endpoint для получения списка оборудования.
    Для пользователей с расширенным доступом - все оборудование,
    для обычных пользователей - только их оборудование.
    """
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        '=serial_number',
        'model',
        'type__name',
        'manufacturer__name',
        'current_owner__username',
        'inverter_number',
    ]
    ordering_fields = [
        'serial_number',
        'model',
        'type__name',
        'manufacturer__name',
        'current_owner__username'
    ]
    ordering = ['serial_number']

    def get_queryset(self):
        user = self.request.user
        queryset = Equipment.objects.all().select_related('type', 'manufacturer', 'current_owner')
        return queryset if user.is_advanced_access else queryset.filter(current_owner=user)

class EquipmentDetailView(generics.RetrieveAPIView):
    """
        Представление для получения детальной информации об оборудовании
    """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'public_id'


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
