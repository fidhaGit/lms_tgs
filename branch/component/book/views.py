from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from superadmin.component.user.authentication import CustomJWTAuthentication
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter


class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = []
    http_method_names = ['get', 'post', 'put']
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ != 'Users':
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        role = user.role.name.lower()
        if role not in ('super_admin', 'admin', 'librarian'):
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        data = request.data.copy()
        if role != 'super_admin':
            data['branch'] = user.branch_id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ == 'Users' and user.role.name.lower() in ('super_admin', 'admin', 'librarian'):
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
        qs = self.filter_queryset(Book.objects.filter(is_delete=False))
        if role == 'super_admin':
            pass
        elif role in ('admin', 'librarian'):
            qs = qs.filter(branch_id=user.branch_id)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        if not (user.__class__.__name__ == 'Users' and user.role.name.lower() in ('super_admin', 'admin')):
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response({'status': 'success', 'message': ["Book removed"]}, status=200)