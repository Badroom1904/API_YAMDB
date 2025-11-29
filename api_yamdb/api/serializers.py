from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from users.models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    """Настройки выдачи пользователей."""
    class Meta:
        model = MyUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def create(self, validated_data):
        """Валидируем создание пользователя."""

        user = MyUser.objects.create(**validated_data)
        user.set_unusable_password()  # Ставим пустой пароль.
        return user


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('username', 'email')

    def create(self, validated_data):
        user = MyUser.objects.create(**validated_data)
        user.set_unusable_password()
        send_mail(
            subject='User registration',
            message=f'Код доступа: {user.confirmation_code}',
            from_email='yamdb@example.com',
            recipient_list=[user.email],
            fail_silently=True,
        )
        return user

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Работа с токеном."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        """Сверяем код и выдаем токен."""

        user = get_object_or_404(MyUser, username=attrs.get('username'))
        if user.confirmation_code != attrs.get('confirmation_code'):
            raise serializers.ValidationError(
                'Неверный код подтверждения.'
            )
        self.context['token'] = AccessToken.for_user(user)
        return attrs

    def to_representation(self, instance):
        """Переопределяем выдачу."""

        return {
            'token': str(self.context['token'])
        }

    def create(self, validated_data):
        """Создаем метод для работы дженериков."""

        return validated_data
