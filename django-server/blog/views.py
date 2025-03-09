from rest_framework import permissions, viewsets
from .models import Post
from .serializers import PostSerializers


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.filter(status="published", is_active=True)

    def perform_create(self, serializer):
        try:
            post = serializer.save()
            self.log_action("Post Created", post)
        except Exception as e:
            self.log_error("Post creation failed", e)
            raise e

    def perform_update(self, serializer):
        try:
            post = serializer.save()
            self.log_action("Post Updated", post)
        except Exception as e:
            self.log_error("Post update failed", e)
            raise e

    def perform_destroy(self, instance):
        try:
            instance.delete()
            self.log_action("Post Deleted", None)
        except Exception as e:
            self.log_error("Post deletion failed", e)
            raise e


class UserPostViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
