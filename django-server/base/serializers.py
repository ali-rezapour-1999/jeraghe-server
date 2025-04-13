from rest_framework import serializers

from user.serializers import UserInformationSerializer
from .models import Skill, Tags, Category, Contact


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


class SkillSerializer(serializers.ModelSerializer):
    skill_reference = TagsSerializer(read_only=True)
    user = UserInformationSerializer(read_only=True)

    class Meta:
        model = Skill
        fields = ["id", "user", "skill_reference", "moon", "year", "level"]
