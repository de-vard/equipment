from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import pyotp
import qrcode
import base64
from io import BytesIO
from django.contrib.auth import get_user_model

User = get_user_model()


class EndeetKeyView(APIView):
    """Для использования indeed key"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Генерация QR-кода для Endeet Key"""
        user = request.user

        # Если секретный ключ не установлен (хотя должен быть по default=pyotp.random_base32)
        if not user.otp_secret:
            user.otp_secret = pyotp.random_base32()
            user.save()

        # Генерация URI для QR-кода (стандарт OTPAuth)
        totp_uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(
            name=user.email,
            issuer_name="Контроль оборудования"  # Замените на название вашего приложения
        )

        # Создание QR-кода
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(totp_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Конвертация в base64 для отправки на фронтенд
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return Response({
            'qr_code': img_str,
            'secret': user.otp_secret,  # Для ручного ввода
            'manual_setup_uri': totp_uri  # Для отладки
        })

    def post(self, request):
        """Проверка кода подтверждения от Endeet Key"""
        user = request.user
        code = request.data.get('code')

        if not code:
            return Response(
                {'error': 'Код подтверждения не предоставлен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.otp_secret:
            return Response(
                {'error': 'Секретный ключ не сгенерирован. Сначала получите QR-код.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверка кода с допуском ±30 секунд (стандартное окно для TOTP)
        totp = pyotp.TOTP(user.otp_secret)
        if totp.verify(code, valid_window=1):  # valid_window=1 означает ±30 секунд
            return Response({
                'status': 'success',
                'message': 'Endeet Key успешно привязан к аккаунту'
            })
        else:
            return Response(
                {'error': 'Неверный код подтверждения. Убедитесь, что время на устройстве синхронизировано.'},
                status=status.HTTP_400_BAD_REQUEST
            )