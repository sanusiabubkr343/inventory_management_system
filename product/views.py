from rest_framework import viewsets
from .models import Product
from .serializers import ListProductSerializer,CreateProductSerializer
from user.permissions import IsAdmin,IsRegularUser


class ProductViewSets(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("created_by").all()
    http_method_names = ["get","post","patch","put","delete"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return ListProductSerializer
        return CreateProductSerializer

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [IsRegularUser()]
        return [IsAdmin()]
