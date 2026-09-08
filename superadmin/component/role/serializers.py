from .models import Role
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = ('created_at', 'updated_at', 'is_active')