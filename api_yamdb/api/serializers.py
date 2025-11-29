from django.core.mail import send_mail
from rest_framework import serializers

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
