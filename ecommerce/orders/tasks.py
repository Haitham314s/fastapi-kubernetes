from celery import shared_task

from .mail import order_notification


@shared_task
def send_email(email: str):
    return order_notification(email)
