from rest_framework import serializers
from .models import Tags, Category


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["title"]

        extra_kwargs = {"title": {"validators": []}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]
