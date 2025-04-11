from rest_framework import serializers
from .models import Tags, Category, Contact


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["title"]

        extra_kwargs = {"title": {"validators": []}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "user", "platform", "link", "is_verified"]
