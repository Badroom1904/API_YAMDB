from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AuthCreateView, AuthViewSet, MyUserViewSet

router_v1 = SimpleRouter()
router_v1.register('users', MyUserViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', AuthCreateView.as_view()),
]
