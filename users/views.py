# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from users.services import send_email_confirm_new_email, send_email_reset_password
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    RequestPasswordResetSerializer,
    PasswordResetConfirmSerializer,
    ChangeEmailRequestSerializer,
)

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class RegisterView(APIView):
    """Регистрация пользователя"""

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Подтвердите email."}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    """Логин (JWT)"""

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            return Response(
                {"error": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST
            )

        refresh_token = RefreshToken.for_user(user)

        return Response(
            {
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token),
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    """Просмотр и обновление профиля"""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(APIView):
    def get(self, request, user_id):
        user: AbstractUser = get_object_or_404(User, id=user_id)
        if not user.is_email_confirmed:
            user.is_email_confirmed = True
            user.save()
            return Response(
                {"message": "Email успешно подтвержден"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Email уже подтвержден"}, status=status.HTTP_400_BAD_REQUEST
        )


class RequestPasswordResetView(APIView):
    """Отправляет ссылку на email для сброса пароля"""

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        # Отправка письма
        send_email_reset_password.delay(email, user)
      
  
        return Response(
            {"message": "Ссылка на сброс пароля отправлена"}, status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    """Обрабатывает переход по ссылке сброса пароля"""

    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, id=user_id)

            if not default_token_generator.check_token(user, token):
                return Response(
                    {"error": "Неверный или устаревший токен"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response(
                {"message": "Пароль успешно изменен"}, status=status.HTTP_200_OK
            )
 
        except Exception:
            return Response(
                {"error": "Неверный запрос"}, status=status.HTTP_400_BAD_REQUEST
            )


class ChangeEmailRequestView(APIView):
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию

    def post(self, request):
        serializer = ChangeEmailRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.is_authenticated:
            return Response(
                { "error": "Пользователь не аутентифицирован"},
                  status=status.HTTP_401_UNAUTHORIZED,
               )
        
        new_email = serializer.validated_data["new_email"]
        
        send_email_confirm_new_email.delay(new_email, user)

        return Response(
            {"message": "Ссылка для подтверждения отправлена на новый email"},
            status=status.HTTP_200_OK,
        )


class ConfirmNewEmailView(APIView):
    """Подтверждает смену email пользователя"""

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        new_email = request.GET.get(
            "new_email"
        )  # Ожидаем, что он будет в GET-параметрах

        if not new_email:
            return Response(
                {"error": "Не передан новый email"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.email = new_email
        user.is_email_confirmed = True
        user.save()

        return Response({"message": "Email успешно изменен"}, status=status.HTTP_200_OK)
