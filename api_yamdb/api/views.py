from rest_framework import permissions, generics, viewsets

from . import serializers
from users.models import MyUser


class MyUserViewSet(viewsets.ModelViewSet):
    """Операции над пользователем (Admin)."""
    queryset = MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer
    lookup_field = 'username'


class AuthCreateView(generics.CreateAPIView):
    """Создание пользователя."""
    queryset = MyUser.objects.all()
    serializer_class = serializers.AuthSerializer
    permission_classes = [permissions.AllowAny]


class CreateTokenView(generics.CreateAPIView):
    """Создаем токен."""
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.TokenSerializer
