from rest_framework import serializers
from .models import Profile, Experience
from user.serializers import UserInformationSerializer


class ExperienceSerializer(serializers.ModelSerializer):
    user = UserInformationSerializer(read_only=True)

    class Meta:
        model = Experience
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
            "description",
        ]
