from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework import response, serializers
from rest_framework.validators import UniqueValidator

from accounts.models import PasswordResetToken
from accounts.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)
from drfauthstartertemplate.settings.base import DOMAIN, EMAIL_USER

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializing the User model
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    avatar = serializers.ImageField(use_url=True, required=False)
    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "avatar",
            "contact",
            "about",
            "is_verified",
            "is_staff",
            "is_superuser",
            "is_active",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = True
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True, write_only=True)


class PasswordResetTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No user is associated with this email address."
            )
        return value

    def create(self, validated_data):
        email = validated_data.get("email")
        user = User.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        reset = PasswordResetToken.objects.create(user=user, token=token)
        reset_link = f"{DOMAIN}/reset-password/{reset.token}/"
        send_mail(
            "Password Reset",
            f"Click the link to reset your password: {reset_link}",
            EMAIL_USER,
            [user.email],
        )
        reset.save()

        return response.Response({"message": "Password reset email sent"})
