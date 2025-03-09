from django.forms.fields import uuid
from django.core.exceptions import ValidationError
import re


def generate_unique_id():
    return uuid.uuid4().hex[:21]


def validate_iranian_phone_number(value):
    if not re.match(r"^(?:0)?9\d{9}$", value):
        raise ValidationError("Enter a valid Iranian phone number.")
