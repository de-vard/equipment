# # transfer/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from .models import TransferRequest
#
#
# @receiver(post_save, sender=TransferRequest)
# def send_transfer_request_notification(sender, instance, created, **kwargs):
#     """
#     Отправляет уведомление при создании новой заявки на передачу техники
#     """
#     if created and instance.receiver.email:  # Только для новых заявок и если есть email
#         # Формируем контекст для шаблона
#         context = {
#             'request': instance,
#             'sender': instance.sender.get_full_name(),
#             'receiver': instance.receiver.get_full_name(),
#             'equipment': instance.equipment,
#             'link': f"https://ваш-сайт.ru/transfer/{instance.public_id}/"
#         }
#
#         # Текстовая версия письма
#         text_message = render_to_string('emails/transfer_request.txt', context)
#
#         # HTML версия письма
#         html_message = render_to_string('emails/transfer_request.html', context)
#
#         # Отправка письма
#         send_mail(
#             subject=f'Новая заявка на передачу техники #{instance.id}',
#             message=text_message,
#             from_email=None,  # Используется DEFAULT_FROM_EMAIL
#             recipient_list=[instance.receiver.email],
#             html_message=html_message,
#             fail_silently=False
#         )