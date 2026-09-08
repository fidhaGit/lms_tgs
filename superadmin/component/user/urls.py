from django.urls import path
from rest_framework import routers
from .views import LoginView, ProfileView, UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
urlpatterns += router.urls