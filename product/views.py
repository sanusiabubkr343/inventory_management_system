from rest_framework import viewsets,filters,status
from .models import Product
from .serializers import ListProductSerializer,CreateProductSerializer
from user.permissions import IsAdmin,IsRegularUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.pagination import CustomPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

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
        elif self.action == 'generate_low_stock_report':
            return None
        else:
            return  CreateProductSerializer

    def paginate_results(self, queryset, serializer=None):
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer if not serializer else serializer
        if page is not None:
            serializer = serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializer(queryset, many=True)
        return Response(serializer.data)
    

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [IsAuthenticated()]
        return [IsAdmin()]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="quantity",
                description="e.g 10(quantity less than 10)",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ],
    )
    @action(
        methods=['POST'],
        detail=False,
        serializer_class=None,
        permission_classes=[IsAdmin],
        url_path='generate-low-stock-report',
    )
    def generate_low_stock_report(self,request,pk=None):
        """endpoint for generating a report of all products that are low in stock with respect to input qunatity,e,g report with quantity less than 10"""
        try:
            quantity = int(request.query_params["quantity"])
        except ValueError:
            return Response(
                data={"error": "Invalid quantity format. Please enter a numeric value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity <=0:
            return Response(data={"error":"quantity must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)
        products = Product.objects.filter(quantity__lt=quantity).select_related("created_by").all()
        return self.paginate_results(products,ListProductSerializer)
