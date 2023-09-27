from rest_framework import serializers
from .models import Substrate, Microorganism, Product


class SubstrateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Substrate
        fields = '__all__'


class MicroorganismSerializer(serializers.ModelSerializer):

    class Meta:
        model = Microorganism
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'