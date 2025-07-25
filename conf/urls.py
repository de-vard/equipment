"""
URL configuration for conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


from authentication.views import LoginViewSet
from equipment.views import EquipmentViewSet

router = routers.DefaultRouter()


router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'auth/login', LoginViewSet, basename='authentication-login')
router.register(r'user', LoginViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/v1/', include(router.urls)),

    # Дополнительные URLs для transfer_request
    path('api/v1/transfer/', include('transfer_request.urls')),

    # Если нужно добавить equipment-specific URLs
    path('api/v1/equipment-/', include('equipment.urls')),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
