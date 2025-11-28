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
        user.save()
        return user
