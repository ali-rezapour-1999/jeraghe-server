from rest_framework import generics, permissions, response, status

from .models import Idea
from .serializer import IdeaSerializer


class CreateIdeaView(generics.CreateAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                idea = serializer.save(user=request.user)
                return response.Response(
                    {"message": "ایدت با موفقیت ثبت شده", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )

            return response.Response(
                {
                    "message": "تو مسیر ثبت ایدت با خطا مواجه شدیم",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return response.Response(
                {
                    "message": "خطایی رخ داده!",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateIdeaView(generics.UpdateAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "idea_update"

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                idea = serializer.save(user=request.user)
                return response.Response(
                    {
                        "message": "تغییرات ایده با موفقیت ثبت شد.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

            return response.Response(
                {
                    "message": "در مسیر اعمال تغییرات ایده خطایی رخ داد.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Idea.DoesNotExist:
            return response.Response(
                {"message": "ایده مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return response.Response(
                {
                    "message": "خطای غیرمنتظره‌ای رخ داد!",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
