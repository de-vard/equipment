# Generated by Django 5.2.1 on 2025-07-25 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Указывает, не уволен ли пользователь', verbose_name='Работает ли пользователь'),
        ),
    ]
