from rest_framework import routers
from .views import RoleViewset

router = routers.SimpleRouter()
router.register(r'roles', RoleViewset, basename='role')
urlpatterns = []
urlpatterns += router.urls