from base.validate import validate_required_field
from rest_framework.validators import ValidationError


def validate_login(data):
    validate_required_field(data.get("email"), "ایمیل")
    validate_required_field(data.get("password"), "رمز عبور")

    return data


def validate_register(data):
    validate_required_field(data.get("email"), "ایمیل")
    validate_required_field(data.get("username"), "نام کاربری")
    validate_required_field(data.get("password"), "رمز عبور")

    if data.get("password") != data.get("confirm_password"):
        raise ValidationError("رمز عبور و تکرار رمز عبور مطابقت ندارند.")

    if data.get("password").length() < 6:
        raise ValidationError("رمز عبور باید حداقل 6 کاراکتر باشد.")

    return data
