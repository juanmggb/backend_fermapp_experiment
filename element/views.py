from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Substrate, Microorganism, Product
from .serializers import SubstrateSerializer, MicroorganismSerializer, ProductSerializer


@api_view(["GET", "POST"])
def microorganism_list(request):
    if request.method == "GET":
        microorganisms = Microorganism.objects.all().order_by("-id")
        serializer = MicroorganismSerializer(microorganisms, many=True)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = MicroorganismSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
def substrate_list(request):
    if request.method == "GET":
        substrates = Substrate.objects.all().order_by("-id")
        serializer = SubstrateSerializer(substrates, many=True)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = SubstrateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all().order_by("-id")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
