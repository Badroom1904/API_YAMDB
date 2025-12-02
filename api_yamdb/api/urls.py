from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuthView, TokenView, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

extra_patterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', AuthView.as_view()),
    path('auth/token/', TokenView.as_view()),
]

urlpatterns = [
    path('v1/', include(extra_patterns))
from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
]
