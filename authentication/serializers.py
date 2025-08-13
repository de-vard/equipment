from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from user.serializers import UserSerializer


class LoginSerializer(TokenObtainPairSerializer):
    """
        Кастомный сериализатор для аутентификации пользователей.
        Наследуется от TokenObtainPairSerializer и добавляет:
        1. Информацию о пользователе в ответ
        2. Обновление времени последнего входа
    """

    def validate(self, attrs):
        data = super().validate(
            attrs)  # проверит email/username и пароль, установит self.user и вернет словарь с access/refresh токенами
        refresh = self.get_token(self.user)  # Генерируем JWT токен для текущего пользователя
        data['user'] = UserSerializer(self.user,
                                      context=self.context).data  # Добавляем в ответ сериализованные данные пользователя
        data['refresh'] = str(refresh)  # Долгоживущий токен для обновления
        data['access'] = str(refresh.access_token)  # Короткоживущий токен доступа

        # Обновляем время последнего входа пользователя (если включено в настройках)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        # Возвращаем полный набор данных: информация о пользователе refresh токен access токен
        return data
