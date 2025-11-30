from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from users.models import MyUser


class BaseSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        """Валидация username при создании и обновлении."""

        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено'
            )
        return value

    def validate_role(self, value):
        """Валидация role на изменение."""

        if self.context.get('request').user.role != 'admin':
            raise serializers.ValidationError(
                'Только администратор может менять роли.'
            )
        return value

    def create(self, validated_data):
        """Создание пользователя и отправка письма."""

        user = MyUser.objects.create(**validated_data)
        user.set_unusable_password()
        user.save()
        send_mail(
            subject='Верификация',
            message=f'Код доступа: {user.confirmation_code}',
            from_email='yamdb@example.com',
            recipient_list=[user.email],
            fail_silently=True,
        )
        return user


class MyUserSerializer(BaseSerializer):
    """Настройки выдачи пользователей."""
    class Meta:
        model = MyUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class AuthSerializer(BaseSerializer):
    """Настройки выдачи при регистрации."""
    class Meta:
        model = MyUser
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    """Работа с токеном."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        """Валидация и выдача токена."""

        user = get_object_or_404(MyUser, username=attrs.get('username'))
        if user.confirmation_code != attrs.get('confirmation_code'):
            raise serializers.ValidationError('Неверный код подтверждения.')
        access_token = AccessToken.for_user(user)
        return {'token': str(access_token)}
