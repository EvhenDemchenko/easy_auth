from celery import shared_task
from django.core.mail import send_mail
from core import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


@shared_task
def send_email_confirmation(user_id, user_email):
    """Отправка письма для подтверждения email"""
    subject = "Подтверждение email"
    message = (
        f"Перейдите по ссылке: http://localhost:8000/users/confirm-email/{user_id}/"
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])


@shared_task
def send_email_reset_password(email, token, uid):


    reset_link = (
        f"http://localhost:8000/users/password-reset-confirm/{uid}/{token}/"
    )

    # Отправка письма
    send_mail(
        "Сброс пароля",
        f"Привет, перейдите по ссылке, чтобы сбросить пароль: {reset_link}",
        "noreply@example.com",
        [email],
        fail_silently=False,
    )


@shared_task
def send_email_confirm_new_email(new_email, user_id):
    confirm_link = f"http://localhost:8000/users/confirm-new-email/{user_id}/?new_email={new_email}"

    send_mail(
        "Подтверждение нового email",
        f"Привет, перейдите по ссылке, чтобы подтвердить новый email: {confirm_link}",
        "noreply@example.com",
        [new_email],
        fail_silently=False,
    )