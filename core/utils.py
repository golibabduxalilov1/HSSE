import uuid
from django.utils.text import slugify


def generate_unique_code(prefix="", length=8):
    unique_id = str(uuid.uuid4())[:length]
    return f"{prefix}{unique_id}".upper() if prefix else unique_id.upper()


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"uploads/{instance.__class__.__name__.lower()}/{filename}"
