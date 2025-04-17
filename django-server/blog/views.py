from rest_framework import permissions, response, status, generics, throttling
from .models import Post
from .serializers import PostSerializers


class CreatePostView(generics.CreateAPIView):
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "post"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)

            return response.Response(
                {"message": "پست با موفقیت ساخته شد", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return response.Response(
            {"message": "ایجاد پست با خطا مواجه شد", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdatePostView(generics.UpdateAPIView):
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "update"

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                {"message": "تغییرات مورد نظر اعمال شده", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return response.Response(
            {
                "message": "ایجاد تغییرات پست با خطا مواجه شد",
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ListPostView(generics.ListAPIView):
    queryset = Post.objects.filter(is_approve=True, status="published")
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "get"


class UserListPostView(generics.ListAPIView):
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "get"

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class GetPostView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(is_approve=True, status="published")
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "get"
