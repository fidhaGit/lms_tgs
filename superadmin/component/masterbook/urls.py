from django.urls import path
from rest_framework import routers
from .views import MasterBookViewset

router = routers.SimpleRouter()
router.register(r'masterbooks', MasterBookViewset, basename='masterbook')

urlpatterns = []
urlpatterns += router.urls