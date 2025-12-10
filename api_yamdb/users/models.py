from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

ROLE_CHOICES = (
    (ROLE_USER, 'Аутентифицированный пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор'),
)

CONFIRMATION_CODE_LENGTH = 6
ROLE_MAX_LENGTH = 10


class User(AbstractUser):
    """Custom user model."""

    email = models.EmailField(
        'Email адрес',
        unique=True,
        blank=False
    )

    role = models.CharField(
        'Роль',
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )

    bio = models.TextField(
        'Биография',
        blank=True
    )

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True
    )

    @property
    def is_admin(self):
        """Return True if user is admin or superuser."""
        return self.role == ROLE_ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Return True if user is moderator."""
        return self.role == ROLE_MODERATOR
