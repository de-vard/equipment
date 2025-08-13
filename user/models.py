import pyotp
from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from base.models.bases import BaseModel, NamedModel


class Position(NamedModel):
    """Должность пользователя"""

    description = models.TextField(blank=True, verbose_name="Описание должности")

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return self.name


class CustomUser(AbstractUser, BaseModel):
    """
    Кастомная модель пользователя, расширяющая стандартную AbstractUser.
    Добавляет дополнительные поля для системы аутентификации и профиля.
    """

    first_name = models.CharField("Имя", max_length=150, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, verbose_name="Отчество", blank=True, default='')
    phone = PhoneNumberField(blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Должность")
    organization = models.ForeignKey('equipment.LegalEntity', on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name="Организация")
    email = models.EmailField(verbose_name="Email адрес", unique=True, blank=False,
                              help_text="Обязательное поле. Введите действующий email адрес.")
    is_work = models.BooleanField(default=True, verbose_name="Работает ли пользователь",
                                  help_text="Указывает, не уволен ли пользователь")
    # Флаг расширенного доступа к системе
    is_advanced_access = models.BooleanField(default=False, verbose_name="Доступ к расширенной информации",
                                             help_text="Указывает, имеет ли пользователь доступ к расширенным данным")

    # Секретный ключ для двухфакторное аутентификации
    # Todo: сделать его шифрованным
    otp_secret = models.CharField(
        max_length=32,
        verbose_name="Секретный ключ для пользователя",
        default=pyotp.random_base32,  # Автогенерация ключа при создании
        help_text="Код для регистрации в приложении Authenticator",
        editable=False  # Запрет редактирования через админку/формы
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['last_name', 'first_name']  # Сортировка по фамилии и имени

    def __str__(self):
        """Строковое представление пользователя (ФИО)"""
        return f"{self.last_name} {self.first_name} {self.middle_name}"
