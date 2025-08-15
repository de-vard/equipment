from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from authentication.endeet_key import EndeetKeyView
from authentication.views import LoginViewSet, RefreshViewSet

from equipment.views import UserEquipmentListView, EquipmentDetailView, \
    EquipmentExportView, AvailableForTransferEquipmentListView, EquipmentListView
from transfer_request.views import TransferEquipmentHistoryView

from user.views import UserOrganizationViewSet

router = routers.DefaultRouter()


router.register(r'auth/login', LoginViewSet, basename='authentication-login')
router.register(r'auth/refresh', RefreshViewSet, basename='authentication-refresh')
router.register(r'users/organization', UserOrganizationViewSet, basename='user-organization')


urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/v1/', include(router.urls)),

    # Дополнительные URLs для transfer_request
    path('api/v1/transfer/', include('transfer_request.urls')),

    # Дополнительные URLs для equipment
    path('api/v1/equipment/',include('equipment.urls')),

    # Для 2-факторной авторизации
    path('api/v1/auth/endeet-key/', EndeetKeyView.as_view(), name='endeet-key'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
