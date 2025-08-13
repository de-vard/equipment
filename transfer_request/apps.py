from django.apps import AppConfig


class TransferRequestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transfer_request'

    def ready(self):
        # Импортируем сигналы при загрузке приложения
        import transfer_request.signals
