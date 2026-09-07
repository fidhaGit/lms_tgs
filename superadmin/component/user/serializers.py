from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Users
from django.contrib.auth.hashers import make_password, check_password


class UserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Users
        fields="__all__"


    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
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