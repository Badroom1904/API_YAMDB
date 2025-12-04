from rest_framework import (
    decorators, filters, permissions,
    response, status, views, viewsets, mixins
)

from .permissions import AdminOrMeOnly, IsAdminOrReadOnly
from .serializers import AuthSerializer, TokenSerializer, User, UserSerializer, CategorySerializer, GenreSerializer
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Title
from .filters import TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = [AdminOrMeOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @decorators.action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """Обработка запросов просмотра или редактирование своего профиля."""

        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return response.Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(serializer.data)


class AuthView(views.APIView):
    """Функция для регистрации пользователя."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Обработка запросов на создание пользователя."""

        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class TokenView(views.APIView):
    """Функция для работы с токеном."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Обработка запросов на создание токена."""

        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            return response.Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete']


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    # def get_serializer_class(self):
    #     if self.action in ('create', 'update', 'partial_update'):
    #         return TitleWriteSerializer
    #     return TitleReadSerializer
