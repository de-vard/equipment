from django.contrib import admin
from .models import Equipment, EquipmentType, Manufacturer,  LegalEntity

from django.utils.html import format_html


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'type', 'manufacturer', 'current_owner', 'display_qr_code', 'display_barcode')
    search_fields = ('serial_number',)
    list_filter = ('type', 'manufacturer')
    readonly_fields = ('display_qr_code', 'display_barcode')  # Делаем поля только для чтения

    def display_qr_code(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="100" height="100" style="border:1px solid #eee" />',
                obj.qr_code.url
            )
        return "-"

    display_qr_code.short_description = 'QR-код'

    def display_barcode(self, obj):
        if obj.barcode:
            return format_html(
                '<img src="{}" width="200" height="100" style="border:1px solid #eee" />',
                obj.barcode.url
            )
        return "-"

    display_barcode.short_description = 'Штрихкод'


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


