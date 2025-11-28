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

    def save(self, *args, **kwargs):
        """
        Сохраняем суперпользователя при создании с ролью admin.
        """

        if self.is_superuser and self.role != 'admin':
            self.role = 'admin'
        super().save(*args, **kwargs)
