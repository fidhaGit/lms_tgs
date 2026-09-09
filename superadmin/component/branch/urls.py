from django.urls import path
from rest_framework import routers
from .views import BranchViewset
router = routers.SimpleRouter()
router.register(r'branches', BranchViewset, basename='branch')

urlpatterns = []
urlpatterns += router.urls