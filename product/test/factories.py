import factory
from product.models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    price=2.30
    quantity=4
