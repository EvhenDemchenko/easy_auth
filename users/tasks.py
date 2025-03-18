from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_notification(user_email, subscribed_to_email, user_username):
    """
    Отправляет письмо на имейл пользователя на который подписался
    """

    email_message = EmailMessage(
        subject=user_username,
        body=f"user {user_email} subscribet to you !",
        to=[subscribed_to_email],
    )

    email_message.send()
