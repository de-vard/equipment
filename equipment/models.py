from django.db import models
from django.contrib.auth import get_user_model

from base.models.bases import BaseModel, NamedModel

User = get_user_model()


class EquipmentType(NamedModel):
    """
    Модель для хранения типов оборудования (категорий техники).
    Например: Ноутбук, Монитор, Телефон и т.д.
    """
    class Meta(NamedModel.Meta):
        verbose_name = "Тип техники"
        verbose_name_plural = "Типы техники"

class Manufacturer(NamedModel):
    """
    Модель производителей оборудования.
    Например: Lenovo, Acer, Samsung и т.д.
    """
    class Meta(NamedModel.Meta):
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

class LegalEntity(NamedModel):
    """
    Модель юридических лиц (организаций), которым принадлежит оборудование.
    Например: СЗ НЛ, Стройград, Крымстрой и т.д.
    """
    short_name = models.CharField(
        'Короткое название',
        max_length=50,
        help_text='Аббревиатура или короткое название (например: "СЗ НЛ")'
    )

    class Meta:
        verbose_name = "Юридическое лицо"
        verbose_name_plural = "Юридическое лица"

class Equipment(BaseModel):
    """ Основная модель для учета оборудования.
        Содержит все характеристики единицы техники.
    """
    type = models.ForeignKey(
        EquipmentType,  # Ссылка на модель EquipmentType
        on_delete=models.SET_NULL,  # Действие при удалении
        null=True,  # Разрешить NULL значения
        blank=True,  # Разрешить пустое значение в формах
        verbose_name='Тип техники',  # Человеко-читаемое имя
        help_text='Категория оборудования (ноутбук, монитор и т.д.)'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Производитель',
        help_text='Компания-производителя оборудования'
    )
    model = models.CharField('Модель', max_length=255)
    serial_number = models.CharField('Серийный номер',max_length=100, unique=True, db_index=True)
    supplier = models.CharField('Поставщик', max_length=255, blank=True, null=True)
    decommissioned_equipment = models.BooleanField('Списана ли техника', default=False)
    photo = models.ImageField('Фото', upload_to='static/images/%Y/%m/%d', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)


    # TODO: сделать поле обязательным, на данный момент поле не обязательное
    #  так как не кто не предоставил инвентарный номера
    inverter_number = models.CharField('Инвентарный  номер', max_length=100, unique=True, blank=True, null=True)
    invoice_info = models.CharField(
        'Счёт',
        max_length=255,
        blank=True,
        null=True,
        help_text='Реквизиты счета или договора поставки'
    )
    current_owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_equipment',
        verbose_name='Текущий владелец',
        help_text='Сотрудник, за которым закреплено оборудование'
    )
    legal_entity = models.ForeignKey(
        LegalEntity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Юрлицо'
    )


    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудования"




    def __str__(self):
        return f"SN: {self.serial_number}"

