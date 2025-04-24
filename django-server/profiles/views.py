from rest_framework import permissions, viewsets, status, generics, throttling
from rest_framework.response import Response
from django.core.cache import cache

from base.responses import error_response, exception_response, success_response
from .models import Profile, WorkHistory
from .serializers import (
    ProfileSerializer,
    WorkHistorySerializer,
)


class ProfileUpdateView(generics.UpdateAPIView):
    throttle_classes = [throttling.ScopedRateThrottle]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "update"

    def update(self, request, *args, **kwargs):
        try:
            instance = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return error_response(
                message="اطلاعات مشخصات شما پیدا نشد.",
                error_code="profile_not_found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if instance.user != request.user:
            return error_response(
                message="شما اجازه ویرایش این اطلاعات را ندارید.",
                error_code="permission_denied",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProfileSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message="خطا در اعتبارسنجی اطلاعات",
                errors=serializer.errors,
                error_code="validation_error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer.save(user=request.user)
            return success_response(
                message="تغییرات ایده با موفقیت ثبت شد.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return exception_response(e)



class ProfileGetView(generics.RetrieveAPIView):
    throttle_classes = [throttling.ScopedRateThrottle]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "get"


    def get(self, request):
        try:
            instance = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return error_response(
                message="ایده مورد نظر پیدا نشد.",
                error_code="idea_not_found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if instance.user != request.user:
            return error_response(
                message="شما اجازه مشاهده این ایده را ندارید.",
                error_code="permission_denied",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProfileSerializer(instance)
        return success_response(
            message="ایده با موفقیت دریافت شد.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
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
