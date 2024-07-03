from rest_framework import viewsets,filters
from .models import Product
from .serializers import ListProductSerializer,CreateProductSerializer
from user.permissions import IsAdmin,IsRegularUser
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSets(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("created_by").all()
    http_method_names = ["get","post","patch","put","delete"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'name',
        'description',
    ]
    ordering_fields = [
        'created_at',
    ]

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
