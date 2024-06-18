from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from accounts.validators import (
    validate_password_digit,
    validate_password_uppercase,
    validate_password_symbol,
    validate_password_lowercase,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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
        user.save()
        return user