from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import MyUserViewSet

router_v1 = SimpleRouter()
router_v1.register('users', MyUserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
