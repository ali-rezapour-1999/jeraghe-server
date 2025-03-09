from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from log.models import RestLog
from user.models import CustomUser
from dj_rest_auth.registration.views import SocialLoginView
import logging
import requests
from base.utils import generate_unique_id

from .serializers import (
    UserDetailSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)

User = get_user_model()
logger = logging.getLogger("user")


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(slug_id=generate_unique_id())
            refresh = RefreshToken.for_user(user)
            RestLog.objects.create(
                user=user,
                action="User Registration",
                request_data=request.data,
                response_data={
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {"email": user.email, "slug": user.slug_id},
                },
            )
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {"email": user.email, "slug": user.slug_id},
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = User.objects.filter(email=email).first()

            if not user:
                return Response(
                    {"error": "NOT_FOUND"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            user = authenticate(request, email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                RestLog.objects.create(
                    user=user,
                    action="User Login",
                    request_data=request.data,
                    response_data={
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": {"email": user.email, "slug": user.slug_id},
                    },
                )
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": {"email": user.email, "slug": user.slug_id},
                    }
                )
            return Response(
                {"error": "PASSWORD_INVALID"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    lookup_field = "slug_id"
    permission_classes = [AllowAny]

    def perform_get(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        RestLog.objects.create(
            user=request.user,
            action="Get User Data",
            request_data={},
            response_data=serializer.data,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        RestLog.objects.create(
            user=request.user,
            action="اطلاعات کاربر با موفقیت ذخیره شد",
            request_data=request.data,
            response_data=serializer.data,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleLogin(SocialLoginView):
    def post(self, request, *args, **kwargs):
        try:
            access_token = request.data.get("access_token")

            if not access_token:
                return Response(
                    {"error": "NO_GOOGLE_ACCESS_TOKEN"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_info = self.get_google_user_info(access_token)
            logger.debug(f"User info from Google: {user_info}")

            user = self.create_or_update_user(user_info)

            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": access,
                    "user": {
                        "email": user.email,
                        "slug": user.slug_id,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(f"Google login failed: {str(e)}")
            return Response(
                {"error": "GOOGLE_LOGIN_FAILED"}, status=status.HTTP_400_BAD_REQUEST
            )

    def get_google_user_info(self, access_token):
        url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Failed to get user info from Google: {response.text}")

        return response.json()

    def create_or_update_user(self, user_info):
        user, created = User.objects.get_or_create(
            email=user_info["email"],
            defaults={
                "username": user_info["name"].replace(" ", "_").lower(),
                "slug_id": user_info["sub"][:21],
            },
        )
        return user
