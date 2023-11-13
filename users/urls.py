from django.urls import path
from users import views

urlpatterns = [
    # Validate username and create user with member
    path("users/", views.user_list),
    # Update or delete user
    path("users/<int:id>/", views.user_details),
    # Get member
    path("members/", views.member_list),
    path("members/<int:id>/", views.member_details),
    path("directors/", views.director_list),
    path("laboratories/", views.laboratory_list),
    path("laboratories/<int:id>/", views.laboratory_details),
]
