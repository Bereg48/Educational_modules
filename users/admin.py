from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс UserAdmin для отображения," \
    фильтрации и поиска модели User"""
    list_display = ('email', 'phone', 'country', 'roles')
    list_filter = ('email', 'country',)
    search_fields = ('phone',)
