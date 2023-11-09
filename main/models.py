from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Module(models.Model):
    """Модель Module"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=False, verbose_name='пользователь')
    number = models.IntegerField(verbose_name='порядковый номер модуля')
    title = models.CharField(max_length=150, verbose_name='название модуля')
    description = models.TextField(verbose_name='описание модуля')
    is_paid = models.BooleanField(default=False, verbose_name='Модуль оплачен')

    def __str__(self):

        return self.title  # pragma: no cover


    def is_paid_by(self, user):
        return self.is_paid

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['id']


class Section(models.Model):
    """Модель Section (Разделы, которые содержатся в модуле модели Module"""
    number = models.IntegerField(verbose_name='порядковый номер раздела')
    title = models.CharField(max_length=150, verbose_name='название раздела')
    description = models.TextField(verbose_name='описание раздела')
    module = models.ForeignKey('Module', on_delete=models.CASCADE,
                               null=True, verbose_name='Модуль',
                               related_name='sections')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.title  # pragma: no cover


    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['id']

    def can_access(self, user):
        # Проверка, можно ли пользователю получить доступ к разделу
        return self.module.is_paid


class Topic(models.Model):
    """Модель Topic (Темы, которые содержатся в разделе модели Section"""
    number = models.IntegerField(verbose_name='порядковый номер темы')
    title = models.CharField(max_length=150, verbose_name='название темы')
    description = models.TextField(verbose_name='описание темы')
    section = models.ForeignKey('Section', on_delete=models.CASCADE,
                                null=True, verbose_name='Раздел',
                                related_name='topics')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title  # pragma: no cover


    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['id']

    def can_access(self, user):
        return self.section.is_paid and self.section.module.is_paid or \
            self.section.can_access(user)


class Payment(models.Model):
    """Модель Payment (Платеж, которые нужно совершить "\
    для просмотра необходимого модуля модели Module """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)  # pragma: no cover


    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['id']
        unique_together = ['user', 'module']


class UserModuleProgress(models.Model):
    """Модель UserModuleProgress (Прогресс пользователя в модуле)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    progress = models.IntegerField()

    def __str__(self):
        return f'{self.user.email} - {self.module.title} - {self.progress}'

    class Meta:
        verbose_name = 'Прогресс пользователя в модуле'
        verbose_name_plural = 'Прогресс пользователей в модулях'
        ordering = ['id']
        unique_together = ['user', 'module']

    @classmethod
    def update_user_progress(cls, user, module, progress):
        cls.objects.update_or_create(
            user=user, module=module, defaults={'progress': progress}
        )
