from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import Users


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")
        if user_id is None:
            raise AuthenticationFailed("Token contains no user identification")
        try:
            return Users.objects.get(id=user_id, is_active=True)
        except Users.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")