from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=256,
        help_text=_('Укажите название категории')
    )
    slug = models.SlugField(
        _('Слаг'),
        max_length=50,
        unique=True,
        help_text=_('Укажите уникальный слаг категории'),
        validators=[]
    )

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=256,
        help_text=_('Укажите название жанра')
    )
    slug = models.SlugField(
        _('Слаг'),
        max_length=50,
        unique=True,
        help_text=_('Укажите уникальный слаг жанра'),
        validators=[]
    )

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=256,
        help_text=_('Укажите название произведения')
    )
    year = models.IntegerField(
        _('Год выпуска'),
        validators=[
            MaxValueValidator(
                timezone.now().year,
                message=_('Год выпуска не может быть больше текущего.')
            )
        ],
        help_text=_('Укажите год выпуска произведения')
    )
    description = models.TextField(
        _('Описание'),
        blank=True,
        null=True,
        help_text=_('Добавьте описание произведения')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name=_('Категория'),
        blank=True,
        null=True,
        help_text=_('Выберите категорию произведения')
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name=_('Жанры'),
        blank=True,
        help_text=_('Выберите жанр(ы) произведения')
    )

    class Meta:
        verbose_name = _('Произведение')
        verbose_name_plural = _('Произведения')
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year', 'category'],
                name='unique_title'
            )
        ]

    def __str__(self):
        return f'{self.name} ({self.year})'

    @property
    def rating(self):
        """Средний рейтинг произведения на основе отзывов."""
        reviews = self.reviews.all()  # related_name='reviews' в модели Review
        if not reviews:
            return None
        return sum(review.score for review in reviews) // len(reviews)


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name=_('Произведение'),
        related_name='genre_titles'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name=_('Жанр'),
        related_name='genre_titles'
    )

    class Meta:
        verbose_name = _('Связь жанра и произведения')
        verbose_name_plural = _('Связи жанров и произведений')
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_genre_title'
            )
        ]

    def __str__(self):
        return f'{self.title} - {self.genre}'
