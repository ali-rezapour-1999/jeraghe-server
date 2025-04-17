import uuid
from django.core.exceptions import ValidationError
import re


def generate_unique_id():
    return uuid.uuid4().hex[:21]


def validate_iranian_phone_number(value):
    if not re.match(r"^(?:0)?9\d{9}$", value):
        raise ValidationError("Enter a valid Iranian phone number.")


def create_or_update_tags(models, validated_data, instance=None):
    from base.models import Tags

    tags_data = validated_data.pop("tags", [])

    if instance:
        instance.title = validated_data.get("title", instance.title)
        instance.save()
    else:
        instance = models.objects.create(**validated_data)

    instance.tags.clear()
    for tag_data in tags_data:
        if "title" in tag_data and tag_data["title"]:
            tag = Tags.objects.get_or_create(title=tag_data["title"])
            instance.tags.add(tag)

    return instance


def validate_tags(value, serializerr):
    if value is None:
        return []
    if not isinstance(value, list):
        raise serializerr.ValidationError("تگ‌ها باید به صورت لیست ارسال شوند.")
    return value
