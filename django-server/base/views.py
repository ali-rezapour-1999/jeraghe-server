from rest_framework import permissions, generics, response, status
from django.core.cache import cache
from .models import Category
from .serializers import CategorySerializer


class CategoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer

    def get(self):
        cached_data = cache.get("category_list")
        if cached_data:
            return response.Response(cached_data, status=status.HTTP_200_OK)

        categories = Category.objects.all()
        serializer = self.get_serializer(categories, many=True)
        data = serializer.data
        cache.set("category_list", data, timeout=7200)
        return Response(data, status=status.HTTP_200_OK)
