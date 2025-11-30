from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuthView, CreateTokenView, MyUserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', MyUserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', AuthView.as_view()),
    path('v1/auth/token/', CreateTokenView.as_view()),
]
