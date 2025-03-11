from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from log.models import RestLog
from .models import Profile, WorkHistory, SocialMedia, UserSkill
from .serializers import (
    ProfileSerializer,
    WorkHistorySerializer,
    SocialMediaSerializer,
    UserSkillSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related("user").filter(is_active=True)
    lookup_field = "user__slug_id"
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        profile = serializer.save()
        cache.delete(f"profile-info/{profile.user.slug_id}")
        RestLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action="Profile Updated",
            request_data=self.request.data,
            response_data=ProfileSerializer(profile).data,
        )


class WorkHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = WorkHistorySerializer
    lookup_field = "user__slug_id"
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkHistory.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def perform_create(self, serializer):
        work_history = serializer.save()
        cache.delete("work_history")
        RestLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action="Work History Created",
            request_data=self.request.data,
            response_data=WorkHistorySerializer(work_history).data,
        )

    def perform_update(self, serializer):
        work_history = serializer.save()
        cache.delete("work_history")
        RestLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action="Work History Updated",
            request_data=self.request.data,
            response_data=WorkHistorySerializer(work_history).data,
        )

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete("work_history")
        RestLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action="Work History Deleted",
            request_data=self.request.data,
            response_data={"id": instance.id},
        )


class SocialMediaViewSet(viewsets.ModelViewSet):
    serializer_class = SocialMediaSerializer
    lookup_field = "slug_id"
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SocialMedia.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def perform_create(self, serializer):
        social_media = serializer.save(user=self.request.user)
        cache.delete("social-media")
        RestLog.objects.create(
            user=self.request.user,
            action="SocialMedia Created",
            request_data=self.request.data,
            response_data=SocialMediaSerializer(social_media).data,
        )

    def perform_update(self, serializer):
        social_media = serializer.save()
        cache.delete("social-media")
        RestLog.objects.create(
            user=self.request.user,
            action="SocialMedia Updated",
            request_data=self.request.data,
            response_data=SocialMediaSerializer(social_media).data,
        )

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete("social-media")
        RestLog.objects.create(
            user=self.request.user,
            action="SocialMedia Deleted",
            request_data=self.request.data,
            response_data={"id": instance.id},
        )


class UserSkillViewSet(viewsets.ModelViewSet):
    serializer_class = UserSkillSerializer
    lookup_field = "user__slug_id"
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SocialMedia.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def perform_create(self, serializer):
        user_skill = serializer.save()
        cache.delete(f"user_skills_{self.request.user.id}")
        RestLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action="User Skill Created",
            request_data=self.request.data,
            response_data=UserSkillSerializer(user_skill).data,
        )

    def perform_update(self, serializer):
        user_skill = serializer.save()
        cache.delete(f"user_skills_{self.request.user.id}")
        RestLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action="User Skill Updated",
            request_data=self.request.data,
            response_data=UserSkillSerializer(user_skill).data,
        )

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(f"user_skills_{self.request.user.id}")
        RestLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action="User Skill Deleted",
            request_data=self.request.data,
            response_data={"id": instance.id},
        )
