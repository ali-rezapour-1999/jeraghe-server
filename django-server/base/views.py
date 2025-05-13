from django.db.models import QuerySet
from rest_framework import permissions, generics, response, status, throttling, viewsets
from rest_framework.views import Response
from .models import Category, Contact, Skill
from .serializers import CategorySerializer, ContactSerializer, SkillSerializer


class CategoryView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ContactCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid():
                contact = serializer.save(user=request.user)

                return response.Response(
                    {
                        "message": "اطلاعات تماس با موفقیت ثبت شد.",
                        "data": ContactSerializer(contact).data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return response.Response(
                {
                    "message": "خطا در اعتبارسنجی اطلاعات تماس.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return response.Response(
                {
                    "message": "خطایی در هنگام ذخیره اطلاعات رخ داده است.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "uploads"

    def get_queryset(self) -> QuerySet[Skill]:  # type: ignore
        return Skill.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid:
            serializer.save(user=self.request.user)
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
        return Response(
            {"message": "آیتم مورد نظر با موفقیت حذف شد"},
            status=status.HTTP_204_NO_CONTENT,
        )
