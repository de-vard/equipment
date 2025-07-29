from rest_framework import serializers

from equipment.models import EquipmentType, Manufacturer, LegalEntity, Equipment
from user.serializers import UserSerializer


class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class LegalEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalEntity
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    type = EquipmentTypeSerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    legal_entity = LegalEntitySerializer(read_only=True)
    current_owner = UserSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = 'public_id','type','manufacturer','model','serial_number','supplier','decommissioned_equipment','photo','created_at','inverter_number', 'invoice_info','current_owner','legal_entity'
