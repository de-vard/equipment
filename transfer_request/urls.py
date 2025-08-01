from django.urls import path
from transfer_request import views

urlpatterns = [
    path('create/', views.TransferRequestCreateView.as_view(), name='transfer-create'),
    path('incoming/', views.IncomingTransferRequestsView.as_view(), name='incoming-transfers'),
    path('pending-incoming/', views.PendingIncomingTransferRequestsView.as_view(), name='pending-incoming-transfers'),
    path('outgoing/', views.OutgoingTransferRequestsView.as_view(), name='outgoing-transfers'),
    path('pending-outgoing/', views.PendingOutgoingTransferRequestsView.as_view(), name='pending-outgoing-transfers'),
    path('requests/<int:pk>/', views.TransferRequestDetailView.as_view(), name='transfer-detail'),
    path('update/<int:pk>/', views.TransferRequestUpdateView.as_view(), name='transfer-update'),
]