from rest_framework import serializers
from user.models import CustomUser
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            slug_id=validated_data["slug_id"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


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
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                "رمز عبور جدید و تأیید آن با هم تطابق ندارند."
            )
        return data

    def save(self, user):
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
