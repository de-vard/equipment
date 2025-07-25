from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name', 'organization','position', 'email','is_advanced_access', 'is_work')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'organization',
        'is_staff',
        'is_active',
        'is_work',
        'is_advanced_access',
    ]
    search_fields = ['username', 'email', 'organization']
