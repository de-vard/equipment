# Импорт необходимых модулей Django REST Framework
from rest_framework import viewsets, status  # viewsets для ViewSet, status для HTTP-статусов
from rest_framework.permissions import AllowAny  # Разрешение доступа без аутентификации
from rest_framework.response import Response  # Для формирования HTTP-ответов
from rest_framework.viewsets import ViewSet  # Базовый класс ViewSet
from rest_framework_simplejwt.views import TokenRefreshView  # Стандартное view для обновления токенов

# Импорт кастомного сериализатора и исключений JWT
from authentication.serializers import LoginSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class LoginViewSet(ViewSet):
    """
    ViewSet для обработки аутентификации пользователей.
    Обрабатывает POST-запросы для входа по email/username и паролю.
    """

    # Указываем какой сериализатор использовать
    serializer_class = LoginSerializer

    # Разрешаем доступ без аутентификации (для входа)
    permission_classes = (AllowAny,)

    # Ограничиваем только POST-методом (вход - создание сессии)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для аутентификации пользователя.

        Args:
            request: HTTP-запрос с данными для входа
            *args: дополнительные позиционные аргументы
            **kwargs: дополнительные именованные аргументы

        Returns:
            Response: HTTP-ответ с токенами и данными пользователя или ошибкой
        """

        # Инициализируем сериализатор с данными запроса
        # context передает request в сериализатор для дополнительной обработки
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        try:
            # Валидируем данные (email/username и пароль)
            # raise_exception=True автоматически вызовет исключение при ошибке валидации
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Если возникла ошибка токена (например, неверные учетные данные)
            # Преобразуем в стандартное исключение InvalidToken
            raise InvalidToken(e.args[0])

        # Возвращаем успешный ответ с валидированными данными:
        # - access токен
        # - refresh токен
        # - данные пользователя
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    """
    ViewSet для обновления JWT-токенов.
    Наследует стандартное TokenRefreshView и добавляет ViewSet-функционал.
    Обрабатывает POST-запросы для обновления access токена по refresh токену.
    """

    # Разрешаем доступ без аутентификации
    permission_classes = (AllowAny,)

    # Ограничиваем только POST-методом
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для обновления токенов.

        Args:
            request: HTTP-запрос с refresh токеном
            *args: дополнительные позиционные аргументы
            **kwargs: дополнительные именованные аргументы

        Returns:
            Response: HTTP-ответ с новыми токенами или ошибкой
        """

        # Получаем стандартный сериализатор из TokenRefreshView
        serializer = self.get_serializer(data=request.data)

        try:
            # Валидируем refresh токен
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Обрабатываем ошибки токена (например, истек или неверный формат)
            raise InvalidToken(e.args[0])

        # Возвращаем новые токены:
        # - новый access токен
        # - (опционально) новый refresh токен, если настроена ротация
        return Response(serializer.validated_data, status=status.HTTP_200_OK)