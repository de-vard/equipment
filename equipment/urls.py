from django.urls import path

from .views import EquipmentDetailWithHistoryView, UserEquipmentListView

urlpatterns = [
    path('with_history/<uuid:pk>/', EquipmentDetailWithHistoryView.as_view(), name='equipment-with-history'),
]
