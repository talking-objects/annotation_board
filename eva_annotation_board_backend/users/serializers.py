from .models import User
from rest_framework import serializers


class TityUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username",)


class PrivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "id",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
