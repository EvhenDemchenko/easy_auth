from rest_framework import serializers
from django.contrib.auth import get_user_model
from .tokens import create_jwt_pair_for_user
from .services import send_email_confirmation

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """Сериализатор регистрации"""

    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_email_confirmation.delay(user.id, user.email)  # Отправляем письмо
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля"""

    class Meta:
        model = User
        fields = ("id", "email", "username", "avatar", "is_email_confirmed")
        read_only_fields = ("email", "is_email_confirmed")


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Пароли не совпадают")
        return data


class ChangeEmailRequestSerializer(serializers.Serializer):
    new_email = serializers.EmailField()

    def validate_new_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется")
        return value
