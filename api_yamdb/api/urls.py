from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AuthViewSet, CreateTokenView, MyUserViewSet

router_v1 = SimpleRouter()
router_v1.register('users', MyUserViewSet)

router_v1_auth = SimpleRouter()
router_v1_auth.register('signup', AuthViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(router_v1_auth.urls)),
    path('v1/auth/token/', CreateTokenView.as_view())
]
