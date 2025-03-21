from rest_framework import serializers
from base.models import Tags
from .models import Post
from base.serializers import TagsSerializer


class PostSerializers(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = (
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

    def validate_tags(self, value):
        if value is None:
            return []
        return value
