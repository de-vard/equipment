from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',  'middle_name','email', 'is_advanced_access','position']
        read_only_fields = ['is_advanced_access']