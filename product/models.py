from django.db import models
from decimal import Decimal

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True,blank=True)
    created_by = models.ForeignKey("user.User",on_delete=models.CASCADE,related_name="created_products")
    price = models.DecimalField(decimal_places=2,max_digits=10,default=Decimal(0.0))
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"
