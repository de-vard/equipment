from django.contrib import admin

from transfer_request.models import TransferRequest


@admin.register(TransferRequest)
class TransferRequestAdmin(admin.ModelAdmin):
    list_display = ('id','equipment', 'sender', 'receiver', 'status', 'requested_at', 'accepted_at')# Register your models here.