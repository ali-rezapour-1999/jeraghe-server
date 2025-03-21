from rest_framework import permissions, response, status, generics
from .models import Post
from .serializers import PostSerializers


class CreatePostView(generics.CreateAPIView):
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            tags_data = validated_data.pop("tags", [])

            post = serializer.save(user=self.request.user)

            for tag_data in tags_data:
                if "title" in tag_data and tag_data["title"]:
                    try:
                        tag = Tags.objects.get(title=tag_data["title"])
                    except Tags.DoesNotExist:
                        tag = Tags.objects.create(title=tag_data["title"])
                    post.tags.add(tag)
            return response.Response(
                {"message": "پست با موفقیت ساخته شد", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return response.Response(
            {"message": "ایجاد پست با خطا مواجه شد", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
