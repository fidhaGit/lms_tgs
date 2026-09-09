from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import LoginSerializer, UserSerializer,ChangePasswordSerializer
from django.contrib.auth.hashers import make_password
from .models import Users
from .authentication import CustomJWTAuthentication
from superadmin.component.role.models import Role


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {"id": user.id, "email": user.email, "first_name": user.first_name, "role_id": user.role_id,
                      "role_name": user.role.name, "branch_id": user.branch_id, "branch_name": user.branch.name},
        })


class ProfileView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = []

    def get(self, request):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        return Response({
            "id": user.id, "email": user.email,
            "first_name": user.first_name, "last_name": user.last_name,
            "role_name": user.role.name, "branch_name": user.branch.name,
        })


class UserViewset(viewsets.ModelViewSet):
    queryset = Users.objects.filter(is_delete=False).order_by('-created_at')
    serializer_class = UserSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = []
    http_method_names = ['get', 'post', 'put']
    pagination_class = None

    def _target_role_name(self, request):
        role_id = request.data.get('role')
        if not role_id:
            return None
        role_obj = Role.objects.filter(id=role_id).first()
        return role_obj.name.lower() if role_obj else None

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ != 'Users':
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        role = user.role.name.lower()
        target_branch = request.data.get('branch')
        target_role = self._target_role_name(request)

        if role == 'super_admin':
            return super().create(request, *args, **kwargs)

        elif role == 'admin':
            if str(user.branch_id) != str(target_branch):
                return Response({'status': 'failure', 'message': ["You can only create users in your own branch"]}, status=400)
            if target_role not in ('admin', 'librarian', 'member'):
                return Response({'status': 'failure', 'message': ["You cannot assign this role"]}, status=400)
            return super().create(request, *args, **kwargs)

        elif role == 'librarian':
            if str(user.branch_id) != str(target_branch):
                return Response({'status': 'failure', 'message': ["You can only create members in your own branch"]}, status=400)
            if target_role != 'member':
                return Response({'status': 'failure', 'message': ["Librarians can only create members"]}, status=400)
            return super().create(request, *args, **kwargs)

        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ != 'Users':
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        instance = self.get_object()
        role = user.role.name.lower()

        if role == 'super_admin':
            return super().update(request, *args, **kwargs)

        elif role == 'admin':
            if str(user.branch_id) != str(instance.branch_id):
                return Response({'status': 'failure', 'message': ["You can only update users in your own branch"]}, status=400)
            return super().update(request, *args, **kwargs)

        elif role == 'librarian':
            if str(user.branch_id) != str(instance.branch_id) or instance.role.name.lower() != 'member':
                return Response({'status': 'failure', 'message': ["Librarians can only update members in their own branch"]}, status=400)
            return super().update(request, *args, **kwargs)

        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ != 'Users':
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        role = user.role.name.lower()
        qs = Users.objects.filter(is_delete=False)

        if role == 'super_admin':
            pass
        elif role in ('admin', 'librarian'):
            qs = qs.filter(branch_id=user.branch_id)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        return Response(qs.values('id', 'email', 'first_name', 'last_name', 'role', 'branch'))

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ != 'Users':
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        instance = self.get_object()
        role = user.role.name.lower()

        if role == 'super_admin':
            pass
        elif role == 'admin' and str(user.branch_id) == str(instance.branch_id):
            pass
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        instance.is_delete = True
        instance.save()
        return Response({'status': 'success', 'message': ["User removed"]}, status=200)

    @action(methods=['POST'], detail=False, authentication_classes=[CustomJWTAuthentication])
    def check_email(self, request):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ == 'Users' and user.role.name.lower() in ('super_admin', 'admin', 'librarian'):
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
class ChangePasswordView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = []

    def post(self, request):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)

        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user.password = make_password(serializer.validated_data["new_password"])
        user.save()

        return Response({'status': 'success', 'message': ["Password updated successfully"]}, status=200)        