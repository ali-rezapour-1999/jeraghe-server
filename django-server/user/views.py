from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status, throttling
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import CustomUser
from base.utils import generate_unique_id
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from .tasks import send_reset_email

from .serializers import (
    UserInformationSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
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
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "update"

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


class GetUserInformationView(generics.RetrieveAPIView):
    serializer_class = UserInformationSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "get"

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk, is_active=True)

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


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    # ایجاد لینک ریست رمز عبور
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(str(user.pk).encode())
                    domain = get_current_site(request).domain
                    link = f"http://{domain}/reset-password/{uid}/{token}/"

                    send_reset_email.delay(email, link)

            return JsonResponse(
                {
                    "status": "success",
                    "message": "لینک ریست رمز عبور به ایمیل شما ارسال شد.",
                }
            )

    else:
        form = PasswordResetForm()

    return render(request, "password_reset_form.html", {"form": form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {"status": "success", "redirect_url": "/password-reset-complete"}
                )
        else:
            form = SetPasswordForm(user)
        return render(request, "password_reset_confirm.html", {"form": form})
    else:
        return JsonResponse(
            {"status": "error", "redirect_url": "/password-reset-invalid"}
        )
