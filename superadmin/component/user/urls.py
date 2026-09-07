from django.urls import path
from .views import LoginView, ProfileView,ProfileDetailView,ProfileListCreateView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profileinfo/", ProfileListCreateView.as_view(), name="profileinfo-create"),
    path("profileinfo/<int:pk>/", ProfileDetailView.as_view(), name="profileinfo-detail"),
]