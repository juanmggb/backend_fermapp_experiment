from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Member, Laboratory
from .serializers import UserSerializer, LaboratorySerializer
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from users.signals import create_member, save_member


@api_view(["GET", "POST"])
def laboratory_list(request):
    if request.method == "GET":
        laboratories = Laboratory.objects.all().order_by("-id")

        serializer = LaboratorySerializer(laboratories, many=True)

        return Response(serializer.data, status=200)


@api_view(["GET", "POST"])
def user_list(request):
    if request.method == "GET":
        username = request.GET.get("username")

        if username:
            users = User.objects.filter(username=username)
        else:
            users = User.objects.all().order_by("-id")

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=200)

    if request.method == "POST":
        data = request.data

        data["password"] = make_password(data.get("password"))

        # Disconnet signals so django doesn't create the member twice for the same user
        post_save.disconnect(create_member, sender=User)
        post_save.disconnect(save_member, sender=User)

        try:
            user = User.objects.create(
                first_name=data["first_name"].upper(),
                username=data["username"],
                password=make_password(data["password"]),
                is_staff=data["is_staff"],
            )
        except:
            return Response(
                {"error": "Username already exists"},
                status=400,
            )
        # When user is created with the frontend this allows create the member and save his corresponding role and image
        # The function create_member in signals is used to create the member when the user is created with the django panel

        # Manually create Member instance with custom role and image
        role = data.get("role", "Student Researcher")
        image = data.get("image", None)
        laboratory = data.get("laboratory", None)

        if image:
            Member.objects.create(
                user=user, image=image, role=role, laboratory=laboratory
            )
        else:
            Member.objects.create(user=user, role=role, laboratory=laboratory)

        # Reconnect signals
        post_save.connect(create_member, sender=User)
        post_save.connect(save_member, sender=User)

        serializer = UserSerializer(user)

        return Response(serializer.data, status=200)
