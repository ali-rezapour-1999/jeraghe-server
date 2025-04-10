from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


@shared_task
def send_reset_email(user_email, link):
    subject = "درخواست ریست رمز عبور"
    message = render_to_string("password_reset_email.html", {"link": link})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
