from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


@shared_task
def send_email_confirmation(user):
    """Отправка письма для подтверждения email"""
    subject = "Подтверждение email"
    message = (
        f"Перейдите по ссылке: http://localhost:8000/users/confirm-email/{user.pk}/"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


@shared_task
def send_email_reset_password(email, user):

    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)

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
def send_email_confirm_new_email( new_email,user):
    confirm_link = f"http://localhost:8000/users/confirm-new-email/{user.id}/?new_email={new_email}"

    send_mail(
        "Подтверждение нового email",
        f"Привет, перейдите по ссылке, чтобы подтвердить новый email: {confirm_link}",
        "noreply@example.com",
        [new_email],
        fail_silently=False,
    )