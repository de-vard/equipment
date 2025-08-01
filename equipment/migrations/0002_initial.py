# Generated by Django 5.2.1 on 2025-07-25 09:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='current_owner',
            field=models.ForeignKey(blank=True, help_text='Сотрудник, за которым закреплено оборудование', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_equipment', to=settings.AUTH_USER_MODEL, verbose_name='Текущий владелец'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='type',
            field=models.ForeignKey(blank=True, help_text='Категория оборудования (ноутбук, монитор и т.д.)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='equipment.equipmenttype', verbose_name='Тип техники'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='legal_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='equipment.legalentity', verbose_name='Юрлицо'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='manufacturer',
            field=models.ForeignKey(blank=True, help_text='Компания-производителя оборудования', null=True, on_delete=django.db.models.deletion.SET_NULL, to='equipment.manufacturer', verbose_name='Производитель'),
        ),
    ]
