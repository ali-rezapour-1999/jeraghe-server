from rest_framework import permissions, viewsets, status, mixins, throttling
from rest_framework.response import Response
from django.core.cache import cache
from .models import Profile, WorkHistory, SocialMedia, UserSkill
from .serializers import (
    ProfileSerializer,
    WorkHistorySerializer,
    SocialMediaSerializer,
    UserSkillSerializer,
)


class ProfileViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    serializer_class = ProfileSerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "update"

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset().first()
        if not queryset:
            return Response(
                {"message": "پروفایل یافت نشد."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, data=request.data, partial=True)

        if serializer.is_valid():
            profile = serializer.save()
            cache.delete(f"profile-info/{profile.user.slug_id}")
            return Response(
                {"message": "تغییرات با موفقیت اعمال شد", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "خطا در اعمال تغییرات", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class WorkHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = WorkHistorySerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "uploads"

    def get_queryset(self):
        return WorkHistory.objects.get(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            cache.delete("work_history")
            return Response(
                {"message": "ایتم مورد نظر با موفقیت ساخته شده"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "message": "انجام عملیات با خطا نواجه شده لطفا کمی بعد مجدد تلاش کنید",
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete("work_history")
            return Response(
                {"message": "تغییرات با موفقیت اعمال شد", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "خطا در اعمال تغییرات", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, instance):
        instance.delete()
        cache.delete("work_history")


class SocialMediaViewSet(viewsets.ModelViewSet):
    serializer_class = SocialMediaSerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "uploads"

    def get_queryset(self):
        return SocialMedia.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            cache.delete("social-media")
            return Response(
                {"message": "ایتم مورد نظر با موفقیت ساخته شده"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "message": "انجام عملیات با خطا نواجه شده لطفا کمی بعد مجدد تلاش کنید",
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete("social-media")
            return Response(
                {"message": "تغییرات با موفقیت اعمال شد", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "خطا در اعمال تغییرات", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, instance):
        instance.delete()
        cache.delete("social-media")


class UserSkillViewSet(viewsets.ModelViewSet):
    serializer_class = UserSkillSerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "uploads"

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid:
            serializer.save(user=self.request.user)
            cache.delete("user-skill")
            return Response(
                {"message": "ایتم مورد نظر با موفقیت ساخته شده"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "message": "انجام عملیات با خطا نواجه شده لطفا کمی بعد مجدد تلاش کنید",
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete("user-skill")
            return Response(
                {"message": "تغییرات با موفقیت اعمال شد", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "خطا در اعمال تغییرات", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, instance):
        instance.delete()
        cache.delete("user-skill")
