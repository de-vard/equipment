from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from authentication.endeet_key import EndeetKeyView
from authentication.views import LoginViewSet, RefreshViewSet

from equipment.views import EquipmentViewSet, UserEquipmentListView, EquipmentDetailWithHistoryView, \
    EquipmentExportView, AvailableForTransferEquipmentListView
from transfer_request.views import TransferRequestCreateView
from user.views import UserOrganizationViewSet

router = routers.DefaultRouter()

router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'auth/login', LoginViewSet, basename='authentication-login')
router.register(r'auth/refresh', RefreshViewSet, basename='authentication-refresh')
router.register(r'users/organization', UserOrganizationViewSet, basename='user-organization')
router.register(r'user', LoginViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/v1/', include(router.urls)),

    # Дополнительные URLs для transfer_request
    path('api/v1/transfer/', include('transfer_request.urls')),

    # Для 2-факторной авторизации
    path('api/v1/auth/endeet-key/', EndeetKeyView.as_view(), name='endeet-key'),

    # Если нужно добавить equipment-specific URLs
    path('api/v1/equip/history/<uuid:public_id>/', EquipmentDetailWithHistoryView.as_view(),
         name='equipment-with-history'),

    # список оборудования
    path('api/v1/equip/my/', UserEquipmentListView.as_view(), name='user-equipment'),

    # список оборудования без статуса ожидания
    path('api/v1/equip/my-without-poisoned/', AvailableForTransferEquipmentListView.as_view(), name='user-equipment'),

    path('api/v1/equip/export/', EquipmentExportView.as_view(), name='equipment-export'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
