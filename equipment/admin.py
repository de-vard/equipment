from django.contrib import admin
from .models import Equipment, EquipmentType, Manufacturer,  LegalEntity

from django.utils.html import format_html


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'type', 'manufacturer', 'current_owner', 'decommissioned_equipment')
    search_fields = ('serial_number',)
    list_filter = ('type', 'manufacturer')


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(LegalEntity)
class LegalEntityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


