from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import CustomUser
from base.utils import generate_unique_id

from .serializers import (
    UserInformationSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            username = serializer.validated_data["username"]

            if User.objects.filter(email=email).first():
                return Response(
                    {
                        "message": "با این ایمیل قبلا حساب زدی برو لاگین کن",
                        "error": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if User.objects.filter(username=username).exists():
                return Response(
                    {
                        "message": "با این نام کاربری قبلا حساب زده شده یکی چی دیگه رو امتحان کن",
                        "error": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = serializer.save(slug_id=generate_unique_id())
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "به جرقه خوش آومدی",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = User.objects.filter(email=email).first()

            if not user:
                return Response(
                    {"message": "با این ایمیل پیدات نکردم مطمئتی درسته؟"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            user = authenticate(request, email=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "message": "خوش برگشتی",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )
            return Response(
                {"message": "رمز عبور اشتباه زدی"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserInformationView(generics.UpdateAPIView):
    serializer_class = UserInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.pk, is_active=True)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "تغییرات با موفقیت اعمل شد", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "خطایی در اعمال تغییرات صورت گرفته لطفا بعدا مجدد تکرار کنید",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetUserInformationView(generics.UpdateAPIView):
    serializer_class = UserInformationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.pk, is_active=True)

    def get(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "دریافت اطلاعات", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "در دریافت اطاعات با مشکل مواجه شدیم",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
