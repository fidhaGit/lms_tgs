from rest_framework import viewsets
from rest_framework.response import Response
from superadmin.component.user.authentication import CustomJWTAuthentication
from .models import BookCopy
from .serializers import BookCopySerializer


class BookCopyViewset(viewsets.ModelViewSet):
    queryset = BookCopy.objects.filter(is_delete=False)
    serializer_class = BookCopySerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = []
    http_method_names = ['get', 'post', 'put']
    pagination_class = None

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        elif user.__class__.__name__ == 'Users' and user.role.name.lower() in ('super_admin', 'admin', 'librarian'):
            return super().create(request, *args, **kwargs)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

    def update(self, request, *args, **kwargs):
        # Used for status changes: mark a copy lost, damaged, retired, etc.
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
        qs = BookCopy.objects.filter(is_delete=False)
        if role == 'super_admin':
            pass
        elif role in ('admin', 'librarian'):
            qs = qs.filter(book__branch_id=user.branch_id)
        else:
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        return Response(qs.values('id', 'book_id', 'copy_code', 'status', 'condition_notes'))

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.__class__.__name__ == 'AnonymousUser':
            return Response({'status': 'failure', 'message': ["Unknown user"]}, status=401)
        if not (user.__class__.__name__ == 'Users' and user.role.name.lower() in ('super_admin', 'admin')):
            return Response({'status': 'failure', 'message': ["Do not have permission to perform this action"]}, status=400)

        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response({'status': 'success', 'message': ["Book copy removed"]}, status=200)