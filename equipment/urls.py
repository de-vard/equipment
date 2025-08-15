from django.urls import path


from equipment.views import UserEquipmentListView, EquipmentDetailView, \
    EquipmentExportView, AvailableForTransferEquipmentListView, EquipmentListView
from transfer_request.views import TransferEquipmentHistoryView



urlpatterns = [
    # список оборудования
    path('', EquipmentListView.as_view(), name='equipment-list'),

    path('my/', UserEquipmentListView.as_view(), name='user-equipment'),

    path('detail/<uuid:public_id>/', EquipmentDetailView.as_view(),name='equipment-detail'),



    # список оборудования без статуса ожидания
    path('my-without-poisoned/', AvailableForTransferEquipmentListView.as_view(), name='available-equipment'),

    # для скачивания эксель
    path('export/', EquipmentExportView.as_view(), name='equipment-export'),
]