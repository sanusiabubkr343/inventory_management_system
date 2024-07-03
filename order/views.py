from rest_framework import viewsets, mixins, status,filters
from rest_framework.decorators import action
from .models import Order, OrderItem
from .serializers import (
    OrderCreationSerializer,
    OrderDetailSerializer,
    OrderItemCreateSerializer,
    OrderItemListSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.permissions import IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404


class OrderViewSets(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.select_related("owner").prefetch_related("orderitem_set").all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['owner', 'status']
    search_fields = [
        'orderitem__product__name',
        'orderitem__product__description',
    ]
    ordering_fields = [
        'created_at',
    ]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return self.queryset
        return self.queryset.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return OrderDetailSerializer
        elif self.action == 'modify_item':
            return OrderItemCreateSerializer
        elif self.action == 'create_order_with_items':
            return OrderCreationSerializer
        else:
            return None

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='create-order-with-items',
    )
    def create_order_with_items(self, request, pk=None):
        """Create order together with the items/product"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            response = {
                "message": "Order Created Successfully",
                **OrderDetailSerializer(instance=order).data,
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAdmin],
        serializer_class=None,
        url_path='complete-order',
    )
    def complete_order(self, request, pk=None):
        """set order to completed"""
        order = self.get_object()
        order.status = "completed"
        order.save()
        response = {
            "message": "Order status completed successfully",
        }
        return Response(data=response, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAdmin],
        serializer_class=None,
        url_path='cancel-order',
    )
    def cancel_order(self, request, pk=None):
        """set order to cancelled"""
        order = self.get_object()
        order.status = "cancelled"
        order.save()
        response = {
            "message": "Order status cancelled successfully",
        }
        return Response(data=response, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAdmin],
        url_path='set-pending',
        serializer_class=None,
    )
    def set_pending(self, request, pk=None):
        """set order to pending"""
        order = self.get_object()
        order.status = "pending"
        order.save()
        response = {
            "message": "Order status pending successfully",
        }
        return Response(data=response, status=status.HTTP_200_OK)

    @action(
        methods=['PATCH'],
        detail=True,
        serializer_class=OrderItemCreateSerializer,
        permission_classes=[IsAuthenticated],
        url_path=r'order-items/(?P<item_id>[\w-]+)/modify-item',
    )
    def modify_item(self, request,item_id, pk=None):
        """modifiy selected item"""
        order = self.get_object()
        order_item = get_object_or_404(OrderItem, pk=item_id)
        serializer = OrderItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_item.order=order
        order_item.product = serializer.validated_data['product']
        order_item.quantity_required = serializer.validated_data['quantity_required']
        order_item.total_price = serializer.validated_data['total_price']
        order_item.save()
       
        response = {
            "message": "Order item updated successfully",
            **OrderItemListSerializer(order_item).data,
        }
        return Response(data=response, status=status.HTTP_200_OK)
