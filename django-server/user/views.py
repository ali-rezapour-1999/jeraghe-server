from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status, throttling, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from base.utils import generate_unique_id
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from user.models import TokenLog
from django.contrib.auth.tokens import PasswordResetTokenGenerator


from .serializers import (
    UserInformationSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    ResetPasswordSerializer,
    SetPasswordSerializer,
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "register"

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            username = serializer.validated_data["username"]

            if User.objects.filter(email=email).exists():
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
                        "message": "با این نام کاربری قبلا حساب زده شده یکی دیگه رو امتحان کن",
                        "error": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = serializer.save(slug_id=generate_unique_id())
            refresh = RefreshToken.for_user(user)
            TokenLog.objects.create(
                user=user,
                access_token=str(refresh.access_token),
                refresh_token=str(refresh),
                expires_at=timezone.now() + timedelta(days=1),
            )
            user_serializer = UserInformationSerializer(user)

            return Response(
                {
                    "message": "به جرقه خوش آومدی",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = User.objects.filter(email=email).first()

            if not user:
                return Response(
                    {"message": "با این ایمیل پیدات نکردم مطمئنی درسته؟"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            user = authenticate(request, email=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                TokenLog.objects.create(
                    user=user,
                    access_token=str(refresh.access_token),
                    refresh_token=str(refresh),
                    expires_at=timezone.now() + timedelta(days=1),
                )
                user_serializer = UserInformationSerializer(user)

                return Response(
                    {
                        "message": "خوش برگشتی",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": user_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "رمز عبور اشتباه زدی"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            access = serializer.validated_data["access"]
            refresh = request.data.get("refresh")

            user = self.get_user_from_token(refresh)

            TokenLog.objects.create(
                user=user,
                access_token=access,
                refresh_token=refresh,
                expires_at=timezone.now() + timedelta(days=1),
            )

            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_user_from_token(self, token):
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh_obj = RefreshToken(token)
        return refresh_obj.user


class UpdateUserInformationView(generics.UpdateAPIView):
    serializer_class = UserInformationSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "update"

    def get_object(self):  # type: ignore
        return User.objects.get(pk=self.request.user.pk, is_active=True)

    def get(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "message": "دریافت اطلاعات",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class GetUserInformationView(generics.RetrieveAPIView):
    serializer_class = UserInformationSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "get"

    def get_object(self):  # type: ignore
        return User.objects.get(pk=self.request.user.pk, is_active=True)

    def get(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"message": "دریافت اطلاعات", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = request.data["email"]
            user = User.objects.filter(email__iexact=email).first()

            if user:
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                domain = get_current_site(request).domain
                uid = urlsafe_base64_encode(str(user.pk).encode())
                link = f"http://{domain}/reset-password/{uid}/{token}/"

                # send_reset_email.delay(email, link)

                return Response(
                    {
                        "status": "success",
                        "message": "لینک ریست رمز عبور به ایمیل شما ارسال شد.",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "error", "message": "کاربری با این ایمیل یافت نشد."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"status": "error", "message": "اطلاعات ورودی نامعتبر است."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PasswordResetConfirmView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = SetPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return Response(
                {
                    "status": "success",
                    "message": "لینک ریست رمز عبور معتبر است.",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "error", "message": "لینک ریست رمز عبور نامعتبر است."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(
                    {"status": "success", "message": "رمز عبور با موفقیت تغییر کرد."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"status": "error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"status": "error", "message": "لینک ریست رمز عبور نامعتبر است."},
            status=status.HTTP_400_BAD_REQUEST,
        )
