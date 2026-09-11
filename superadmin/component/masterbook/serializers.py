from rest_framework import serializers
from .models import MasterBook


class MasterBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterBook
        exclude = ('created_at', 'updated_at', 'is_delete')