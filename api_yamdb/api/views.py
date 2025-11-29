from rest_framework import response, views, viewsets
from rest_framework_simplejwt.tokens import AccessToken

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
    http_method_names = ['post', 'patch']

