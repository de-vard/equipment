from django.db import models
import uuid

class BaseModel(models.Model):
    public_id = models.UUIDField(
        db_index=True,  # Ускоряет поиск по public_id.
        unique=True,  # Запрещает дубликаты.
        default=uuid.uuid4,  # Автоматически генерирует UUID.
        editable=False,  # Нельзя изменить вручную.
    )
    class Meta:
        abstract = True

class NamedModel(BaseModel):
    """
    Абстрактная модель для объектов с именем.
    Содержит стандартное поле name и базовую логику.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название',
        help_text='Уникальное название объекта'
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']  # Сортировка по умолчанию по имени