from rest_framework import serializers
from .models import Profile, WorkHistory, SocialMedia, UserSkill
from base.serializers import TagsSerializer
from user.serializers import UserInformationSerializer


class SocialMediaSerializer(serializers.ModelSerializer):
    user = UserInformationSerializer(read_only=True)

    class Meta:
        model = SocialMedia
        fields = ["user", "title", "address", "slug_id"]


class UserSkillSerializer(serializers.ModelSerializer):
    skill_reference = TagsSerializer(read_only=True)
    user = UserInformationSerializer(read_only=True)

    class Meta:
        model = UserSkill
        fields = ["id", "user", "skill_reference", "moon", "year", "level"]


class WorkHistorySerializer(serializers.ModelSerializer):
    user = UserInformationSerializer(read_only=True)

    class Meta:
        model = WorkHistory
        fields = [
            "user",
            "job_title",
            "company_name",
            "start_date",
            "end_date",
            "job_description",
            "is_working",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "slug_id",
            "gender",
            "age",
            "state",
            "city",
            "address",
            "desciption",
        ]
