from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Substrate, Microorganism, Product
from .serializers import SubstrateSerializer, MicroorganismSerializer, ProductSerializer
from django.db.models import Q
from .utilis.element import filter_dict, filter_dict_product


@api_view(["GET", "POST"])
def microorganism_list(request):
    if request.method == "GET":
        print("GET", request.GET)

        filterby = request.GET.get("filterby", "")
        search = request.GET.get("search", "")
        sortby = request.GET.get("sortby", "")

        filters = Q()
        if filterby and search:
            filters = Q(**{f"{filter_dict[filterby]}__icontains": search})

        queryset = Microorganism.objects.filter(filters)

        queryset = queryset.order_by(filter_dict.get(sortby, "-id"))

        serializer = MicroorganismSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = MicroorganismSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def microorganism_details(request, id):
    try:
        microorganism = Microorganism.objects.get(id=id)
    except Microorganism.DoesNotExist:
        return Response(
            {"message": "Microorganism with given id doesn't exists"}, status=404
        )

    if request.method == "GET":
        serializer = MicroorganismSerializer(microorganism)

        return Response(serializer.data, status=200)

    elif request.method == "PUT":
        serializer = MicroorganismSerializer(data=request.data, instance=microorganism)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        print(serializer.errors)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        microorganism.delete()

        return Response(
            {"message": "Microorganism has been deleted successfully"}, status=200
        )


@api_view(["GET", "POST"])
def substrate_list(request):
    if request.method == "GET":
        print("GET", request.GET)

        filterby = request.GET.get("filterby", "")
        search = request.GET.get("search", "")
        sortby = request.GET.get("sortby", "")

        filters = Q()
        if filterby and search:
            filters = Q(**{f"{filter_dict[filterby]}__icontains": search})

        queryset = Substrate.objects.filter(filters)

        queryset = queryset.order_by(filter_dict.get(sortby, "-id"))

        serializer = SubstrateSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = SubstrateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def substrate_details(request, id):
    try:
        substrate = Substrate.objects.get(id=id)
    except Substrate.DoesNotExist:
        return Response(
            {"message": "Substrate with given id doesn't exists"}, status=200
        )

    if request.method == "GET":
        serializer = SubstrateSerializer(substrate)

        return Response(serializer.data, status=200)

    elif request.method == "PUT":
        serializer = SubstrateSerializer(instance=substrate, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        print(serializer.errors)

        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        substrate.delete()

        return Response({"message": "Substrate deleted successfully"}, status=200)


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        print("GET", request.GET)

        filterby = request.GET.get("filterby", "")
        search = request.GET.get("search", "")
        sortby = request.GET.get("sortby", "")

        filters = Q()
        if filterby and search:
            filters = Q(**{f"{filter_dict_product[filterby]}__icontains": search})

        queryset = Product.objects.filter(filters)

        queryset = queryset.order_by(filter_dict_product.get(sortby, "-id"))

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def product_details(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"message": "Product with given id doesn't exist"}, status=404)

    if request.method == "GET":
        serializer = ProductSerializer(product)

        return Response(serializer.data, status=200)

    elif request.method == "PUT":
        serializer = ProductSerializer(data=request.data, instance=product)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        print(serializer.errors)

        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        product.delete()

        return Response({"message": "Product deleted successfully"}, status=200)
