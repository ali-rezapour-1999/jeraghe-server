from rest_framework import permissions, generics, response, status
from .models import Category, Contact
from .serializers import CategorySerializer, ContactSerializer


class CategoryView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ContactCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Contact.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)

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
