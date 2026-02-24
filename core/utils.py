import uuid
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
import random

def generate_unique_code(prefix="", length=8):
    unique_id = str(uuid.uuid4())[:length]
    return f"{prefix}{unique_id}".upper() if prefix else unique_id.upper()


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"uploads/{instance.__class__.__name__.lower()}/{filename}"


def generate_otp():
    return str(random.randint(100000, 999999))


import threading
from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(email, otp):
    subject = "Email tasdiqlash kodi"
    message = f"Sizning tasdiqlash kodingiz: {otp}"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


def send_otp_email_async(email, otp):
    threading.Thread(
        target=send_otp_email,
        args=(email, otp),
    ).start()