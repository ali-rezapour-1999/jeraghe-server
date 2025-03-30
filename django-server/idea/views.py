from rest_framework import generics, permissions, response, status


class CreateIdeaView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(user=self.request.user)
            return response.Response(
                {"message": "پست با موفقیت ساخته شد", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return response.Response(
            {"message": "ایجاد پست با خطا مواجه شد", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
