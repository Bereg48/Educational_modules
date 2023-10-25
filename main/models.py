from django.db import models

from users.models import User


class Module(models.Model):
    """Модель Module"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    number = models.IntegerField(verbose_name='порядковый номер модуля')
    title = models.CharField(max_length=150, verbose_name='название модуля')
    description = models.TextField(verbose_name='описание модуля')
    is_paid = models.BooleanField(default=False, verbose_name='Модуль оплачен')

    def __str__(self):
        return self.title

    def is_paid_by(self, user):
        return self.paid_users.filter(id=user.id).exists()

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['id']


class Section(models.Model):
    """Модель Section (Разделы, которые содержатся в модуле модели Module"""
    number = models.IntegerField(verbose_name='порядковый номер раздела')
    title = models.CharField(max_length=150, verbose_name='название раздела')
    description = models.TextField(verbose_name='описание раздела')
    module = models.ForeignKey('Module', on_delete=models.CASCADE, null=True, verbose_name='Модуль',
                               related_name='sections')

    def __str__(self):
        return self.title

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
    section = models.ForeignKey('Section', on_delete=models.CASCADE, null=True, verbose_name='Раздел',
                                related_name='topics')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['id']

    def can_access(self, user):
        # Проверка, можно ли пользователю получить доступ к теме
        return self.section.can_access(user)


class Payment(models.Model):
    """Модель Payment (Платеж, которые нужно совершить для просмотра необходимого модуля модели Module """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['id']
