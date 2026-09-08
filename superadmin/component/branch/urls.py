from django.urls import path
from rest_framework import routers
from .views import BranchViewSet

router = routers.SimpleRouter()
router.register(r'branches', BranchViewSet, basename='branch')

urlpatterns = []
urlpatterns += router.urls