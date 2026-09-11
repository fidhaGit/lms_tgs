from django.urls import path
from rest_framework import routers
from .views import BookViewset

router = routers.SimpleRouter()
router.register(r'books', BookViewset, basename='book')

urlpatterns = []
urlpatterns += router.urls