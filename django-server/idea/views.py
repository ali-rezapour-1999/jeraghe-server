from rest_framework import generics, permissions, status
from base.responses import error_response, exception_response, success_response
from .models import Idea
from .serializer import IdeaSerializer


class CreateIdeaView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = IdeaSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message="خطا در اعتبارسنجی اطلاعات",
                errors=serializer.errors,
                error_code="validation_error",
            )
        try:
            idea = serializer.save(user=request.user)
            return success_response(
                message="ایده با موفقیت ثبت شد",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return exception_response(e)


class UpdateIdeaView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "idea_update"

    def update(self, request, *args, **kwargs):
        idea_id = request.data.get("id")

        if not idea_id:
            return error_response(
                message="شناسه ایده ارسال نشده است.",
                error_code="missing_id",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            instance = Idea.objects.get(id=idea_id)
        except Idea.DoesNotExist:
            return error_response(
                message="ایده مورد نظر پیدا نشد.",
                error_code="idea_not_found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if instance.user != request.user:
            return error_response(
                message="شما اجازه ویرایش این ایده را ندارید.",
                error_code="permission_denied",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = IdeaSerializer(instance, data=request.data, partial=True)
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


class GetIdeaView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "get"

    def get(self, request):
        idea_id = request.data.get("id")
        if not idea_id:
            return error_response(
                message="شناسه ایده ارسال نشده است.",
                error_code="missing_id",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            instance = Idea.objects.get(id=idea_id)
        except Idea.DoesNotExist:
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

        serializer = IdeaSerializer(instance)
        return success_response(
            message="ایده با موفقیت دریافت شد.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class DeleteIdeaView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        idea_id = request.data.get("id")
        if not idea_id:
            return error_response(
                message="شناسه ایده ارسال نشده است.",
                error_code="missing_id",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            instance = Idea.objects.get(id=idea_id)
        except Idea.DoesNotExist:
            return error_response(
                message="ایده مورد نظر پیدا نشد.",
                error_code="idea_not_found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if instance.user != request.user:
            return error_response(
                message="شما مجاز به حذف این ایده نیستید.",
                error_code="permission_denied",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        try:
            instance.delete()
            return success_response(
                message="ایده با موفقیت حذف شد.",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return exception_response(e)
