from django.db.models import QuerySet
from rest_framework import permissions, viewsets, status, generics, throttling
from rest_framework.response import Response
from django.core.cache import cache
from .models import Profile, WorkHistory, Skill
from .serializers import (
    ProfileSerializer,
    WorkHistorySerializer,
    SkillSerializer,
)


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "update"

    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset().first()
        token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1]

        if not queryset:
            return Response(
                {"message": "پروفایل یافت نشد."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            cache.delete(f"profile/get/{token}")
            return Response(
                {"message": "تغییرات با موفقیت اعمال شد", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "خطا در اعمال تغییرات", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProfileGetView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "get"

    def get_queryset(self):  # type:ignore
        return Profile.objects.get(user=self.request.user)

    def get(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class WorkHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = WorkHistorySerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "uploads"

    def get_queryset(self):  # type:ignore
        return WorkHistory.objects.get(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def create(self, request):
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
            cache.delete("work-history")
            return Response(
                {"message": "تغییرات با موفقیت اعمال شد", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "خطا در اعمال تغییرات", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        cache.delete("work-history")
        return Response(
            {"message": "آیتم مورد نظر با موفقیت حذف شد"},
            status=status.HTTP_204_NO_CONTENT,
        )
