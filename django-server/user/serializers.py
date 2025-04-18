from rest_framework import serializers
from user import validate
from user.models import CustomUser
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": []},
        }

        def validte_register(self):
            return validate.validate_register(self.data)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    class Meta:
        models = CustomUser
        fields = ["email", "password"]

    def validatetor(self):
        return validate.validate_login(self.data)


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "slug_id", "image", "username"]


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(
        write_only=True, required=True, min_length=8
    )

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.default_detail)
        return value

    def save(self, **kwargs):
        if not hasattr(self, "validated_data") or self.validated_data is None:
            error_msg = "داده‌های معتبر قبل از ذخیره‌سازی باید تأیید شوند."
            raise ValueError(error_msg)

        user = kwargs.get("user")
        if not user:
            error_msg = "کاربر نباید تهی باشد."
            raise ValueError(error_msg)

        new_password = self.validate_new_password("new_password")
        if not new_password:
            error_msg = "رمز عبور جدید وارد نشده است."
            raise ValueError(error_msg)

        user.set_password(new_password)
        user.save()
        return user
