from rest_framework import serializers
from .models import Order,OrderItem
from product.models import Product
from decimal import Decimal

class OrderItemListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = OrderItem


class CustomerProductReportSerializer(serializers.Serializer):
    product = serializers.StringRelatedField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_expenditure_on_product = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    total_quantity_required = serializers.IntegerField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'product_name',
            'total_quantity_required',
            'total_expenditure_on_product',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        expenditure = Decimal(representation['total_expenditure_on_product'])
        representation['total_expenditure_on_product'] = round(expenditure, 2)
        return representation


class OrderDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(source="owner.fullname")
    items =OrderItemListSerializer(many=True,source="orderitem_set")
    class Meta:
        fields = "__all__"
        model=Order


class OrderItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["product", "quantity_required"]
        model = OrderItem

    def validate(self, attrs):
        quantity_required = attrs["quantity_required"]
        if quantity_required <= 0:
            raise serializers.ValidationError("Product quantity must  be greater than zero")

        unit_price = attrs["product"].price

        attrs["total_price"] = round(quantity_required * unit_price, 2)

        return attrs


class OrderCreationSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)

    def validate(self, attrs):
        attrs["owner"] = self.context.get("request").user
        return super().validate(attrs)

    def save(self, **kwargs):
        kwargs["owner"] = self.validated_data["owner"]
        order = Order.objects.create(**kwargs)
        ordered_items = [OrderItem(**item,order=order)  for item in self.validated_data["items"]]
        OrderItem.objects.bulk_create(ordered_items)
        return order
