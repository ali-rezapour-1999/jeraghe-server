from rest_framework import generics, permissions, response, status

from idea.models import Idea


class CreateIdeaView(generics.CreateAPIView):
    queryset = Idea.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(user=self.request.user)
            return response.Response(
                {"message": "ایدت با موفقیت ثبت شده", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return response.Response(
            {
                "message": "تو مسیر ثبت ایدت با خطا مواجه  شدیم",
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateIdeaView(generics.UpdateAPIView):
    queryset = Idea.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(user=self.request.user)
            return response.Response(
                {"message": " تغییرت ایدت با موفقیت ثبت شده", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return response.Response(
            {
                "message": "تو مسیراعمال تغییرات ایدت با خطا مواجه  شدیم",
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
