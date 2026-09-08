from .serializers import RoleSerializer
from .models import Role
from rest_framework import viewsets
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('name').exclude(Q(name="Super Admin") | Q(name="SUPER ADMIN"))
    serializer_class = RoleSerializer
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
        return Response(Role.objects.all().exclude(name="Super Admin").values('id', 'name'))

    @action(methods=['POST'], detail=False)
    def check_name(self, request):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.role.name.lower() == 'super_admin':
            name = request.data.get('name')
            if not name:
                return Response({'status': 'failure', 'message': ["payload not found"]}, status=400)
            role_qs = Role.objects.filter(name__iexact=name)
            if not role_qs:
                return Response({'status': 'success', 'message': ["role not exist"], 'available': True}, status=200)
            else:
                return Response({'status': 'success', 'message': ["role already exist"], 'available': False}, status=200)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)