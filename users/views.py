from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import Laboratory
from .serializers import UserSerializer, LaboratorySerializer
from django.db.models.signals import post_save
from django.db.models import Q
from .utilis.users import filter_by_date, filter_dict, filter_dict_member
from django.db import transaction
from django.contrib.auth import get_user_model


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_account(request):
    try:
        user = request.user
        assert user.is_authenticated
    except:
        return Response({"message": "Authentication is required"}, status=400)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

    elif request.method == "PUT":
        serializer = UserSerializer(data=request.data, instance=user, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        print(serializer.errors)

        return Response(serializer.errors, status=400)


@api_view(["POST"])
def create_user_view(request):
    data = request.data
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=201)
    print(serializer.errors)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
def user_validate_email(request):
    # Validate if email already exist

    email = request.GET.get("email")
    userId = request.GET.get("userId")

    if userId:
        users = get_user_model().objects.filter(email=email).exclude(id=userId).exists()
    else:
        users = get_user_model().objects.filter(email=email).exists()

    if users:
        return Response({"message": "User with given email already exists"}, status=200)

    return Response({"message": "Email is available"}, status=200)


@api_view(["GET"])
def user_list(request):
    users = get_user_model().objects.all()

    serializer = UserSerializer(users, many=True)

    return Response(serializer.data, status=200)


@api_view(["GET", "PUT", "DELETE"])
def user_details(request, id):
    try:
        user = get_user_model().objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message": "User with given id doesn't exist"}, status=404)

    if request.method == "GET":
        serializer = UserSerializer(user)

        return Response(serializer.data, status=200)

    elif request.method == "PUT":
        data = request.data

        serializer = UserSerializer(instance=user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=201)
        print(serializer.errors)
        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        user.delete()

        return Response({"message": "User deleted successfully"}, status=200)


@api_view(["GET", "POST"])
@transaction.atomic
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

        queryset = queryset.order_by(filter_dict.get(sortby, "-id"))

        serializer = LaboratorySerializer(queryset, many=True)

        return Response(serializer.data, status=200)

    elif request.method == "POST":
        data = request.data

        serializer = LaboratorySerializer(data=data)

        if serializer.is_valid():
            laboratory = serializer.save()

            # Assign laboratory to Lab Director
            print("DATA", data)
            director = get_user_model().objects.get(id=data.get("director"))

            if director.laboratory:
                raise ValueError("Director already has a laboratory")
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
        serializer = LaboratorySerializer(
            instance=laboratory, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)

        print(serializer.errors)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        laboratory.delete()

        return Response({"message": "Laboratory deleted successfully"}, status=200)
