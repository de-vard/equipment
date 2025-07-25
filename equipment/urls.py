from django.urls import path

from .views import EquipmentDetailWithHistoryView, UserEquipmentListView

urlpatterns = [
    path('my/', UserEquipmentListView.as_view(), name='user-equipment'),
    path('with-history/<int:pk>/', EquipmentDetailWithHistoryView.as_view(), name='equipment-with-history'),

]
