# Generated by Django 4.2.4 on 2023-11-09 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_section_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='description',
            field=models.TextField(verbose_name='описание модуля'),
        ),
        migrations.AlterField(
            model_name='module',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Модуль оплачен'),
        ),
        migrations.AlterField(
            model_name='module',
            name='title',
            field=models.CharField(max_length=150, verbose_name='название модуля'),
        ),
        migrations.AlterField(
            model_name='section',
            name='description',
            field=models.TextField(verbose_name='описание раздела'),
        ),
        migrations.AlterField(
            model_name='section',
            name='number',
            field=models.IntegerField(verbose_name='порядковый номер раздела'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=models.TextField(verbose_name='описание темы'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='number',
            field=models.IntegerField(verbose_name='порядковый номер темы'),
        ),
        migrations.CreateModel(
            name='UserModuleProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.IntegerField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Прогресс пользователя в модуле',
                'verbose_name_plural': 'Прогресс пользователей в модулях',
                'ordering': ['id'],
                'unique_together': {('user', 'module')},
            },
        ),
    ]