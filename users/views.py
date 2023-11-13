from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Member, Laboratory
from .serializers import (
    UserSerializer,
    LaboratorySerializer,
    DirectorSerializer,
    MemberSerializer,
    ValidateUsernameSerializer,
)
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from users.signals import create_member, save_member
from django.db.models import Q
from .utilis.users import filter_by_date, filter_dict, filter_dict_member


@api_view(["GET", "POST"])
def laboratory_list(request):
    if request.method == "GET":
        print("GET", request.GET)

        filterby = request.GET.get("filterby", "")
        search = request.GET.get("search", "")
        sortby = request.GET.get("sortby", "")
        initialdate = request.GET.get("initialdate", "")
        finaldate = request.GET.get("finaldate", "")

        filters = Q()
        if filterby and search:
            filters = Q(**{f"{filter_dict[filterby]}__icontains": search})

        queryset = Laboratory.objects.filter(filters)

        queryset = filter_by_date(queryset, initialdate, finaldate)

        # laboratories = Laboratory.objects.all().order_by("-id")

        queryset = queryset.order_by(filter_dict.get(sortby, "-id"))

        serializer = LaboratorySerializer(queryset, many=True)

        return Response(serializer.data, status=200)

    elif request.method == "POST":
        data = request.data

        serializer = LaboratorySerializer(data=data)

        if serializer.is_valid():
            laboratory = serializer.save()

            # Assign laboratory to Lab Director
            director = Member.objects.get(id=data.get("director"))
            director.laboratory = laboratory
            director.save()

            return Response(serializer.data, status=200)
        print(serializer.errors)

        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def laboratory_details(request, id):
    try:
        laboratory = Laboratory.objects.get(id=id)
    except Laboratory.DoesNotExist:
        return Response(
            {"message": "Laboratory with given id doesn't exists"}, status=404
        )

    if request.method == "GET":
        serializer = LaboratorySerializer(laboratory)

        return Response(serializer.data, status=200)

    elif request.method == "PUT":
        serializer = LaboratorySerializer(instance=laboratory, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        laboratory.delete()

        return Response({"message": "Laboratory deleted successfully"}, status=200)


@api_view(["GET", "POST"])
def user_list(request):
    # Validate if username already exist
    if request.method == "GET":
        username = request.GET.get("username")
        userId = request.GET.get("userId")

        if userId:
            users = User.objects.filter(username=username).exclude(id=userId)
        else:
            users = User.objects.filter(username=username)
        serializer = ValidateUsernameSerializer(users, many=True)

        return Response(serializer.data, status=200)

    # Create username and member
    if request.method == "POST":
        data = request.data

        mutable_data = data.copy()  # This creates a mutable copy of the QueryDict

        # Now you can change the values as needed
        mutable_data["password"] = make_password(mutable_data.get("password"))

        # data["password"] = make_password(data.get("password"))

        # Disconnet signals so django doesn't create the member twice for the same user
        post_save.disconnect(create_member, sender=User)
        post_save.disconnect(save_member, sender=User)
        role = data.get("role", "Student Researcher")

        try:
            name = data["first_name"].upper()
            user = User.objects.create(
                first_name=name,
                username=data["username"],
                password=make_password(mutable_data["password"]),
                is_staff=role == "Lab Director",
            )
        except:
            return Response(
                {"error": "Username already exists"},
                status=400,
            )
        # When user is created with the frontend this allows create the member and save his corresponding role and image
        # The function create_member in signals is used to create the member when the user is created with the django panel

        # Manually create Member instance with custom role and image
        image = data.get("image", None)

        if image:
            member = Member.objects.create(user=user, name=name, image=image, role=role)
        else:
            member = Member.objects.create(user=user, name=name, role=role)

        laboratoryId = data.get("laboratoryId", None)
        if laboratoryId:
            laboratory = Laboratory.objects.get(id=laboratoryId)
            member.laboratory = laboratory
            member.laboratory_name = laboratory.laboratory_name
            member.save()

        # Reconnect signals
        post_save.connect(create_member, sender=User)
        post_save.connect(save_member, sender=User)

        serializer = UserSerializer(user)

        return Response({"message": "User has been created successfully"}, status=200)


@api_view(["PUT", "DELETE"])
def user_details(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message": "User with given id doesn't exist"}, status=404)

    if request.method == "PUT":
        data = request.data

        print(data)

        # Modify user fields
        if data.get("password"):
            user.password = make_password(data.get("password"))
        user.username = data.get("username", user.username)
        user.first_name = data.get("name", user.first_name)
        user.save()
        # Modify member fields
        member = Member.objects.get(user=user)
        if data.get("laboratoryId"):
            laboratory = Laboratory.objects.get(id=data.get("laboratoryId"))
            member.laboratory = laboratory
            member.laboratory_name = laboratory.laboratory_name
        member.name = data.get("name", member.name)
        member.role = data.get("role", member.role)

        if data.get("image"):
            member.image = data.get("image")

        member.save()

        return Response({"message": "Account updated successfully"}, status=200)

    if request.method == "DELETE":
        user.delete()

        return Response({"message": "User deleted successfully"}, status=200)


@api_view(["GET"])
def member_list(request):
    print("GET", request.GET)

    filterby = request.GET.get("filterby", "")
    search = request.GET.get("search", "")
    sortby = request.GET.get("sortby", "")
    initialdate = request.GET.get("initialdate", "")
    finaldate = request.GET.get("finaldate", "")

    filters = Q()
    if filterby and search:
        filters = Q(**{f"{filter_dict_member[filterby]}__icontains": search})

    queryset = Member.objects.filter(filters)

    queryset = filter_by_date(queryset, initialdate, finaldate)

    # laboratories = Laboratory.objects.all().order_by("-id")

    queryset = queryset.order_by(filter_dict_member.get(sortby, "-id"))

    serializer = MemberSerializer(queryset, many=True)

    return Response(serializer.data, status=200)


@api_view(["GET", "PUT"])
def member_details(request, id):
    try:
        member = Member.objects.get(id=id)
    except Member.DoesNotExist:
        return Response({"message": "Member with given id doesn't exist"}, status=404)

    if request.method == "GET":
        serializer = MemberSerializer(member)

        return Response(serializer.data, status=200)

    elif request.method == "PUT":
        role = request.data.get("role")

        member.role = role

        member.save()

        return Response({"message": "Member role updated successfully"}, status=200)


@api_view(["GET"])
def director_list(request):
    directors = Member.objects.filter(role="Lab Director").order_by("-id")

    serializer = DirectorSerializer(directors, many=True)

    return Response(serializer.data, status=200)
