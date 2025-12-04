from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', verbose_name='Категория', blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles',
        verbose_name='Жанры', blank=True
    )

    def __str__(self):
        return f'{self.name} ({self.year})'
