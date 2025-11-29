from rest_framework import viewsets

from . import serializers
from users.models import MyUser


class MyUserViewSet(viewsets.ModelViewSet):
    """Операции над пользователем (Admin)."""
    queryset = MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer
    lookup_field = 'username'


class AuthViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = serializers.AuthSerializer
