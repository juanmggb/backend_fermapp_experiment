from .models import Laboratory
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AuthTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        data["name"] = user.name
        data["bro"] = "hi"

        return data


# We can use the same serializer for registrering users and updating users
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data.
    This class extends the ModelSerializer to handle user data serialization, focusing on fields like email, password, and name. The password field is set to write-only for security.
    The create method is overriden to utilize the custom user model's create_user method
    """

    laboratory_name = serializers.CharField(
        source="laboratory.laboratory_name", read_only=True
    )

    class Meta:
        model = get_user_model()
        # fields = "__all__"
        fields = [
            "id",
            "email",
            "password",
            "name",
            "role",
            "image",
            "is_staff",
            "laboratory",
            "laboratory_name",
            "created_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        # This is necessary to hash password
        if password:
            user.set_password(password)
            user.save()
        return user


class LaboratorySerializer(serializers.ModelSerializer):
    director_name = serializers.CharField(source="director.name", read_only=True)

    class Meta:
        model = Laboratory
        fields = "__all__"
