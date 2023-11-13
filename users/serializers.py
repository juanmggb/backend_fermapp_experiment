from .models import Member, Laboratory
from django.contrib.auth.models import User

from rest_framework import serializers


class LoginSerializer(serializers.ModelSerializer):
    memberId = serializers.CharField(source="member.id", read_only=True)

    class Meta:
        model = User
        fields = ("memberId", "username")


# Only for validating username
class ValidateUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


# Only for creating a member
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Member
        fields = "__all__"


class DirectorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    # username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Member
        fields = ("id", "first_name")
        # fields = "__all__"


class LaboratoryMemberSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Member
        fields = ("first_name", "role")


class LaboratorySerializer(serializers.ModelSerializer):
    # director_name = serializers.CharField(
    #     source="director.user.first_name",
    #     read_only=True,
    # )

    members = LaboratoryMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Laboratory
        # exclude = ("director",)
        fields = "__all__"
        extra_kwargs = {"director": {"write_only": True}}
