from rest_framework import (
    decorators, filters, permissions,
    response, status, generics, views, viewsets
)

from .permissions import AdminOrMeOnly
from . import serializers
from users.models import MyUser


class MyUserViewSet(viewsets.ModelViewSet):
    """Операции над пользователем (Admin)."""
    queryset = MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = [AdminOrMeOnly]
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

    @decorators.action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return response.Response(serializer.data)
        elif request.method == 'PATCH':
            if request.data.get('role'):
                request.data.pop('role')
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(serializer.data)


class AuthView(views.APIView):
    """Создание пользователя."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.AuthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CreateTokenView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.TokenSerializer(data=request.data)
        if serializer.is_valid():
            return response.Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
