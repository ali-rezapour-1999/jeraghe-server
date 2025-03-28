from rest_framework import permissions, generics, response, status
from django.core.cache import cache
from .models import Category
from .serializers import CategorySerializer


class CategoryView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        cached_data = cache.get("category")
        if cached_data:
            return response.Response(cached_data, status=status.HTTP_200_OK)

        return super().get(request, *args, **kwargs)
