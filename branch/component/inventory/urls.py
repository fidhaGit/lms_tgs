from django.urls import path
from rest_framework import routers
from .views import BookCopyViewset

router = routers.SimpleRouter()
router.register(r'copies', BookCopyViewset, basename='bookcopy')

urlpatterns = []
urlpatterns += router.urls