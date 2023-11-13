# The line data = super().validate(attrs) calls the parent class's validate method, which performs the actual token creation and validation.
# After this call, data will contain the access and refresh tokens.

# After getting the tokens, you are serializing the user data using UserSerializer(self.user).data.
# You then iterate over this serialized data and add it to the data dictionary, which already contains the tokens.
# So, the final data dictionary returned by your validate method includes both the tokens and the additional user information.

from users.serializers import (
    LoginSerializer,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = LoginSerializer(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
