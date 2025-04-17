from rest_framework import serializers


def validate_required_field(value, field_name="این فیلد"):
    if value in [None, "", [], {}, ()]:
        raise serializers.ValidationError(f"{field_name} نمی‌تواند خالی باشد.")
    return value
