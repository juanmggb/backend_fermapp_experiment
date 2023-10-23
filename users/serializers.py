from .models import Member, Laboratory
from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="member.role", read_only=True)
    image = serializers.CharField(source="member.image", read_only=True)
    laboratory = serializers.CharField(
        source="member.laboratory.laboratory_name", read_only=True
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "username",
            "is_staff",
            "password",
            "role",
            "image",
            "laboratory",
        )


class DirectorSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField(source="user.first_name", read_only=True)
    # username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Member
        # fields = ("id", "first_name", "username", "role")
        fields = "__all__"


class LaboratorySerializer(serializers.ModelSerializer):
    director = DirectorSerializer()

    class Meta:
        model = Laboratory
        fields = "__all__"
