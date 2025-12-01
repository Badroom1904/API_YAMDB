from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = [
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class MyUser(AbstractUser):
    """Кастомная модель пользователя."""
    email = models.EmailField('Email адрес', unique=True, blank=False)
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField('Код подтверждения', max_length=6)

    def generate_confirmation_code(self):
        """Сгенерировать новый код подтверждения."""

        self.confirmation_code = str(randint(100000, 999999))

    def save(self, *args, **kwargs):
        """Сохраняем суперпользователя и генерируем код."""

        if self.is_superuser and self.role != 'admin':
            self.role = 'admin'
        super().save(*args, **kwargs)
