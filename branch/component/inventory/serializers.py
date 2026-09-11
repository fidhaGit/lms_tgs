from rest_framework import serializers
from .models import BookCopy


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        exclude = ('created_at', 'updated_at', 'is_delete')
        read_only_fields = ('copy_code',)   # auto-generated, never sent by client