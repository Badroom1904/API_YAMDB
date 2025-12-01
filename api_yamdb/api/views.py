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
