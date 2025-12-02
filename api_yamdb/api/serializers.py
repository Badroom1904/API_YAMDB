from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken


User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор."""
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
            return self.instance.role
        return value

    def create(self, validated_data):
        """Создание пользователя и отправка письма."""

        user = User.objects.create(**validated_data)
        user.set_unusable_password()
        user.generate_confirmation_code()
        send_mail(
            subject='Верификация',
            message=f'Код доступа: {user.confirmation_code}',
            from_email='yamdb@example.com',
            recipient_list=[user.email],
            fail_silently=True,
        )
        user.save()
        return user


class UserSerializer(BaseSerializer):
    """Настройки выдачи пользователей."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class AuthSerializer(BaseSerializer):
    """Настройки выдачи при регистрации."""
    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    """Работа с токеном."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        """Валидация и выдача токена."""

        user = get_object_or_404(User, username=attrs.get('username'))
        if user.confirmation_code != attrs.get('confirmation_code'):
            raise serializers.ValidationError('Неверный код подтверждения.')
        access_token = AccessToken.for_user(user)
        return {'token': str(access_token)}
from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений (с вложенными объектами)."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления произведений (со slug)."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        allow_null=True
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        from django.utils import timezone
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        return value

    def to_representation(self, instance):
        """При выводе используем сериализатор для чтения."""
        return TitleReadSerializer(instance).data
