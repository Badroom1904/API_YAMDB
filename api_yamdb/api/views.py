from rest_framework import (
    decorators, filters, permissions,
    response, status, views, viewsets
)

from .permissions import AdminOrMeOnly
from .serializers import AuthSerializer, TokenSerializer, User, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = [AdminOrMeOnly]
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

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

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets


from reviews.models import Category, Genre, Title
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleReadSerializer, TitleWriteSerializer
)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Кастомный ViewSet, который предоставляет только действия:
    create, list, destroy.
    Используется для категорий и жанров.
    """
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    """ViewSet для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """ViewSet для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleWriteSerializer
        return TitleReadSerializer
