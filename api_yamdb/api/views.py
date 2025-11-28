from rest_framework import viewsets

from . import serializers
from users.models import MyUser


class MyUserViewSet(viewsets.ModelViewSet):
    """Операции над пользователем."""
    queryset = MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer
