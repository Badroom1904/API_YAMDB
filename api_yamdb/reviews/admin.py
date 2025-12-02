from django.contrib import admin
from .models import Category, Genre, Title, GenreTitle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'rating')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('name', 'description')
    inlines = (GenreTitleInline,)
    readonly_fields = ('rating',)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    list_filter = ('genre',)
