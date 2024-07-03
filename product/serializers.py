from rest_framework import serializers
from .models import Product


class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "description", "quantity", "price"]

    def validate(self, attrs):
        quantity = attrs["quantity"]
        price = attrs["price"]

        if quantity <= 0:
            raise serializers.ValidationError("Product quantity must  be greater than zero")

        if price < 0.0:
            raise serializers.ValidationError("Price of a product cannot be less than 0.0")

        return attrs  


class ListProductSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(source="created_by.firstname")
    class Meta:
        model = Product
        fields = "__all__"
