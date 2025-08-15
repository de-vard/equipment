from django.contrib.auth import get_user_model
from django.utils import timezone

from base.models.bases import BaseModel
from django.db import models

from equipment.models import Equipment

User = get_user_model()


class TransferRequest(BaseModel):
    """Передачи оборудования"""
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='transfer_history',
        verbose_name='Оборудование'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_transfers',
        verbose_name='Передавший'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_transfers',
        verbose_name='Получатель'
    )
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,db_index=True, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')
    accepted_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата принятия или отказа от техники')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f"{self.equipment} — от {self.sender} к {self.receiver}"

    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения модели TransferRequest.
        Добавляет автоматическую установку даты принятия/отказа при изменении статуса.
        Таким образом, accepted_at:
        - Устанавливается только при первом изменении статуса на accepted/rejected
        - Не изменяется при последующих обновлениях записи
        - Не сбрасывается при других изменениях (например, редактировании комментария)
        """
        if self.status in ['accepted', 'rejected'] and not self.accepted_at:
            self.accepted_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "История передачи оборудования"
        verbose_name_plural = "История передачи оборудования"

        ordering = ['-requested_at']
