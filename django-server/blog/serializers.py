from rest_framework import serializers
from .models import Post
from base.serializers import TagsSerializer
from base.utils import create_or_update_tags


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
        return create_or_update_tags(Post, validated_data)

    def update(self, instance, validated_data):
        return create_or_update_tags(Post, validated_data, instance=instance)


class GetPostSerializers(serializers.ModelSerializer):
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
