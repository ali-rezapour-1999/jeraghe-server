from rest_framework import serializers
from base.serializers import TagsSerializer
from idea.models import Idea
from user.serializers import UserInformationSerializer


class IdeaSerializer(serializers.ModelSerializer):
    user = UserInformationSerializer(read_only=True)
    tags = TagsSerializer()

    class Meta:
        model = Idea
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "status",
            "needs_collaborators",
            "required_skills",
            "collaboration_type",
            "related_files",
            "tags",
            "category",
            "repo_url",
            "contact_info"
        ]
