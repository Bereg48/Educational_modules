from django.contrib import admin

from main.models import Module, Section, Topic, Payment


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Класс ModuleAdmin для отображения," \
    фильтрации и поиска модели Module"""
    list_display = ('user', 'number', 'title', 'description')
    list_filter = ('title', 'user',)
    search_fields = ('user',)


@admin.register(Section)
class ModuleSection(admin.ModelAdmin):
    """Класс ModuleSection для отображения," \
    фильтрации и поиска модели Section"""
    list_display = ('module', 'number', 'title', 'description')
    list_filter = ('title', 'module',)
    search_fields = ('module',)


@admin.register(Topic)
class ModuleTopic(admin.ModelAdmin):
    """Класс ModuleTopic для отображения," \
     фильтрации и поиска модели Topic"""
    list_display = ('section', 'number', 'title', 'description')
    list_filter = ('title', 'section',)
    search_fields = ('section',)


@admin.register(Payment)
class ModulePayment(admin.ModelAdmin):
    """Класс ModulePayment для отображения," \
    "фильтрации и поиска модели Payment"""
    list_display = ('user', 'module', 'amount', 'payment_date')
    list_filter = ('module', 'amount', 'payment_date',)
    search_fields = ('user',)
