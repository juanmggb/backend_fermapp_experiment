from .models import Substrate, Microorganism, Product
from .serializers import SubstrateSerializer, MicroorganismSerializer, ProductSerializer

from rest_framework.viewsets import ModelViewSet

# Create your views here.


# ModelViewSet for Substrate, Microorganism and Product

class SubstrateViewSet(ModelViewSet):

    queryset = Substrate.objects.all()
    serializer_class = SubstrateSerializer

class MicroorganismViewSet(ModelViewSet):

    queryset = Microorganism.objects.all()
    serializer_class = MicroorganismSerializer


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer