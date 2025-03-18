from django.core.mail import send_mail
from django.conf import settings


def send_email_confirmation(user):
    """Отправка письма для подтверждения email"""
    subject = "Подтверждение email"
    message = (
        f"Перейдите по ссылке: http://localhost:8000/users/confirm-email/{user.pk}/"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
