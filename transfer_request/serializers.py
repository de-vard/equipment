from django.contrib.auth import get_user_model
from rest_framework import serializers

from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer
from transfer_request.models import TransferRequest
from user.serializers import UserSerializer

User = get_user_model()

class TransferRequestSerializer(serializers.ModelSerializer):
    """Базовый сериализатор только для чтения"""
    equipment = EquipmentSerializer(read_only=True)
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = TransferRequest
        fields = ('public_id','equipment','sender','receiver')
        read_only_fields = ['sender', 'requested_at', 'accepted_at', 'status']

class CreateTransferRequestSerializer(serializers.ModelSerializer):
    """Специальный сериализатор для создания заявок"""
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    equipment = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all())

    class Meta:
        model = TransferRequest
        fields = ['equipment', 'receiver', 'comment']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        request = self.context['request']
        equipment = data['equipment']
        receiver = data['receiver']

        if receiver == request.user:
            raise serializers.ValidationError(
                {"receiver": "Нельзя создать заявку самому себе"}
            )

        if equipment.current_owner != request.user:
            raise serializers.ValidationError(
                {"equipment": "Вы не являетесь владельцем этого оборудования"}
            )

        if TransferRequest.objects.filter(
                equipment=data['equipment'],
                sender=self.context['request'].user,
                status='pending'
        ).exists():
            raise serializers.ValidationError("Заявка на это оборудование уже существует.")
        return data

class UpdateTransferRequestSerializer(serializers.ModelSerializer):
    """Специальный сериализатор для обновления статуса"""

    class Meta:
        model = TransferRequest
        fields = ['status', 'comment']
        extra_kwargs = {
            'status': {'required': False},
            'comment': {'required': False}
        }

    def validate(self, data):
        instance = self.instance
        request = self.context['request']

        # Проверяем, что заявка еще в статусе ожидания
        if instance.status != 'pending' and 'comment' in data:
            raise serializers.ValidationError(
                {"status": "Нельзя изменить статус уже обработанной заявки или комментарий"}
            )

        # Проверяем, что пользователь - получатель
        if request.user != instance.receiver:
            raise serializers.ValidationError(
                {"status": "Только получатель может изменить статус заявки"}
            )

        return data

    def update(self, instance, validated_data):
        # Основная логика обновления
        if 'status' in validated_data:
            new_status = validated_data['status']
            instance.status = new_status

            if new_status == 'accepted':
                # Меняем владельца оборудования при принятии
                instance.equipment.current_owner = instance.receiver
                instance.equipment.save()

            elif new_status == 'rejected':
                # Можно добавить дополнительную логику при отклонении
                pass

        if 'comment' in validated_data:
            instance.comment = validated_data['comment']

        instance.save()
        return instance