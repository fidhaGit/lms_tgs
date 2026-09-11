from .serializers import BranchSerializer
from .models import Branch
from rest_framework import viewsets
from rest_framework.response import Response
from superadmin.component.user.authentication import CustomJWTAuthentication
from rest_framework.decorators import action


class BranchViewset(viewsets.ModelViewSet):
    queryset = Branch.objects.filter(is_delete=False).order_by('name')
    serializer_class = BranchSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = []
    http_method_names = ['get', 'post', 'put']
    pagination_class = None

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ == 'Users' and user.role.name.lower() == 'super_admin':
            return super().create(request, *args, **kwargs)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ == 'Users' and user.role.name.lower() == 'super_admin':
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
        qs = Branch.objects.filter(is_delete=False)
        if role == 'super_admin':
            pass
        elif role in ('admin', 'librarian'):
            qs = qs.filter(id=user.branch_id)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)
        return Response(qs.values('id', 'name', 'code', 'address', 'phone', 'email', 'is_active'))

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        if not (user.__class__.__name__ == 'Users' and user.role.name.lower() == 'super_admin'):
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)
        instance = self.get_object()

        if branch_has_dependent_data(instance.id):
            return Response({
                'status': 'failure',
                'message': ["Cannot delete a branch that still has books or members. Remove or reassign them first."]
            }, status=400)

        instance.is_delete = True
        instance.save()
        return Response({'status': 'success', 'message': ["Branch removed"]}, status=200)

    @action(methods=['POST'], detail=False, authentication_classes=[CustomJWTAuthentication])
    def check_code(self, request):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ == 'Users' and user.role.name.lower() == 'super_admin':
            code = request.data.get('code')
            if not code:
                return Response({'status': 'failure', 'message': ["payload not found"]}, status=400)
            exists = Branch.objects.filter(code__iexact=code).exists()
            if not exists:
                return Response({'status': 'success', 'message': ["code not exist"], 'available': True}, status=200)
            else:
                return Response({'status': 'success', 'message': ["code already exist"], 'available': False}, status=200)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)
        