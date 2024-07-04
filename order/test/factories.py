import factory
from order.models import Order,OrderItem


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem
    quantity_required=2
    total_price = 4.23
