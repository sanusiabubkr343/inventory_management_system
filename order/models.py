from django.db import models
from decimal import Decimal
from .enums import ORDER_STATUSES
from product.models import Product
from user.models import User

def default_status():
    return "pending"


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="placed_orders")
    status = models.CharField(max_length=20, choices=ORDER_STATUSES, default=default_status)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Order {self.pk} placed by {self.owner.fullname}"

    class Meta:
        ordering = ('-created_at',)


class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity_required = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=Decimal(0.00))
    order=models.ForeignKey("Order",on_delete=models.CASCADE)

    def __str__(self):
        return f"Order Item {self.pk} for product {self.product.name}"
