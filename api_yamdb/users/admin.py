from django.contrib import admin

from .models import MyUser


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',
                    'role', 'bio', 'first_name', 'last_name')
