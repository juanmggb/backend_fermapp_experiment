from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users import views
from users.serializers import AuthTokenSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = AuthTokenSerializer


app_name = "users"
urlpatterns = [
    # User account
    path("me/", views.user_account, name="me"),
    # Create new account
    path("users/create/", views.create_user_view, name="create"),
    # Validate username and create user with user
    path("username-validate/", views.user_validate_email),
    path("users/", views.user_list, name="user-list"),
    # # Update or delete user
    path("users/<int:id>/", views.user_details),
    #    Laboratories
    path("laboratories/", views.laboratory_list),
    path("laboratories/<int:id>/", views.laboratory_details),
    # Login
    path("users/token/", CustomTokenObtainPairView.as_view(), name="token"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
