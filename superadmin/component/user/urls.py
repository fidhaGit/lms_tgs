from django.urls import path
from rest_framework import routers
from .views import LoginView, ProfileView, UserViewset, ChangePasswordView

router = routers.SimpleRouter()
router.register(r'users', UserViewset, basename='user')

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
urlpatterns += router.urls