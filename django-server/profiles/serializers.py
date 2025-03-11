from rest_framework import serializers
from .models import Profile, WorkHistory, SocialMedia, UserSkill
from base.serializers import TagsSerializer
from user.serializers import UserDetailSerializer


class SocialMediaSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = SocialMedia
        fields = ["user", "title", "address", "slug_id"]


class UserSkillSerializer(serializers.ModelSerializer):
    skill_reference = TagsSerializer(read_only=True)

    class Meta:
        model = UserSkill
        fields = "__all__"


class WorkHistorySerializer(serializers.ModelSerializer):
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
        fields = "__all__"

    def get_email(self, obj):
        return obj.user.email if obj.user else None
