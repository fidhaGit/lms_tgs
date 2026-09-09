from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Users
from django.contrib.auth.hashers import make_password, check_password


from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ('password', 'created_at', 'updated_at')

    def create(self, validated_data):
        raw_password = self.initial_data.get("password")
        validated_data["password"] = make_password(raw_password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        raw_password = self.initial_data.get("password")
        if raw_password:
            validated_data["password"] = make_password(raw_password)
        return super().update(instance, validated_data)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            user = Users.objects.get(email=attrs["email"])
        except Users.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not check_password(attrs["password"], user.password):
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        attrs["user"] = user
        return attrs    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Old password is incorrect.")
        return value