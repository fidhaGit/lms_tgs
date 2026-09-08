from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import LoginSerializer, UserSerializer
from .models import Users


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {"id": user.id, "email": user.email, "first_name": user.first_name},
        })


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id, "email": user.email,
            "first_name": user.first_name, "last_name": user.last_name,
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.filter(is_delete=False).order_by('-created_at')
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put']
    pagination_class = None

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.role.name.lower() == 'super_admin':
            return super().create(request, *args, **kwargs)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.role.name.lower() == 'super_admin':
            return super().update(request, *args, **kwargs)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        return Response(Users.objects.filter(is_delete=False).values('id', 'email', 'first_name', 'last_name', 'role', 'branch'))

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        if user.role.name.lower() != 'super_admin':
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response({'status': 'success', 'message': ["User removed"]}, status=200)

    @action(methods=['POST'], detail=False)
    def check_email(self, request):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.role.name.lower() == 'super_admin':
            email = request.data.get('email')
            if not email:
                return Response({'status': 'failure', 'message': ["payload not found"]}, status=400)
            exists = Users.objects.filter(email__iexact=email).exists()
            if not exists:
                return Response({'status': 'success', 'message': ["email not exist"], 'available': True}, status=200)
            else:
                return Response({'status': 'success', 'message': ["email already exist"], 'available': False}, status=200)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)