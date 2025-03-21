from rest_framework import serializers
from base.models import Tags
from .models import Post
from base.serializers import TagsSerializer


class PostSerializers(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "status",
            "tags",
            "categories",
            "image",
            "views",
            "show_detail",
            "is_approve",
        )

    def create(self, validated_data):
        return self.create_or_update(validated_data)

    def update(self, instance, validated_data):
        return self.create_or_update(validated_data, instance=instance)

    def create_or_update(self, validated_data, instance=None):
        tags_data = validated_data.pop("tags", [])

        if instance:
            instance.title = validated_data.get("title", instance.title)
            instance.save()
        else:
            instance = Post.objects.create(**validated_data)

        instance.tags.clear()
        for tag_data in tags_data:
            if "title" in tag_data and tag_data["title"]:
                tag, created = Tags.objects.get_or_create(title=tag_data["title"])
                instance.tags.add(tag)

        return instance

    def validate_tags(self, value):
        if value is None:
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError("تگ‌ها باید به صورت لیست ارسال شوند.")
        return value
