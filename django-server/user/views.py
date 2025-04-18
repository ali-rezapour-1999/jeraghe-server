from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status, throttling, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from base.responses import error_response, success_response
from base.utils import generate_unique_id
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

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
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "register"

    def create(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                if User.objects.filter(email=request.data["email"]).exists():
                    return error_response(
                        message="با این ایمیل قبلا حساب زده شده یکی دیگه رو امتحان کن",
                        error_code="email_already_exists",
                        errors=serializer.errors,
                    )
                if User.objects.filter(username=request.data["username"]).exists():
                    return error_response(
                        message="با این نام کاربری قبلا حساب زده شده یکی دیگه رو امتحان کن",
                        error_code="username_already_exists",
                    )
                user = serializer.save(slug_id=generate_unique_id())
                refresh = RefreshToken.for_user(user)
                user_serializer = UserInformationSerializer(user)

                return success_response(
                    message="به جرقه خوش آومدی",
                    data={
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": user_serializer.data,
                    },
                )
        except Exception as e:
            return error_response(e)


class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=request.data["email"]).first()

            if not user:
                return error_response(
                    message="با این ایمیل پیدات نکردم مطمئنی درسته؟",
                    error_code="user_not_found",
                )
            if user.check_password(request.data["password"]):
                refresh = RefreshToken.for_user(user)
                user_serializer = UserInformationSerializer(user)
                return success_response(
                    message="خوش برگشتی",
                    data={
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": user_serializer.data,
                    },
                )
            return error_response(
                message="رمز عبور اشتباه است.",
                error_code="invalid_password",
                errors=serializer.errors,
            )


class UpdateUserInformationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "update"

    def get(self, request):
        instance = User.objects.get(pk=request.user.pk, is_active=True)
        serializer = self.UserInformationSerializer(instance)
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

    def get(self, request):
        instance = User.objects.get(pk=request.user.pk, is_active=True)
        serializer = UserInformationSerializer(instance)
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
