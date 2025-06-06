from rest_framework import serializers
from .models import Product  # or your model

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
