from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    MEMBER = 'Member', 'Участник'
    ADMIN = 'Admin', 'Администратор'
    MODERATOR = 'Moderator', 'Модератор'


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона',
                             blank=True, null=True)
    country = models.CharField(max_length=35, verbose_name='Город',
                               blank=True, null=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар',
                               blank=True, null=True)
    roles = models.CharField(max_length=9, choices=UserRoles.choices,
                             default=UserRoles.MEMBER)

    def __str__(self):
        return self.username  # pragma: no cover

    def is_paid_user(self):
        return self.paid_users.exists()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


