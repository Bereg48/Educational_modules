# Generated by Django 4.2.4 on 2023-10-27 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='number',
            field=models.IntegerField(verbose_name='порядковый номер модуля'),
        ),
    ]