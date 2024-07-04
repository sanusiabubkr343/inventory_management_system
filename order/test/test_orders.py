import pytest
from django.urls import reverse
from rest_framework import status
from user.test.factories import UserFactory
from product.test.factories import ProductFactory
from order.test.factories import OrderFactory, OrderItemFactory


pytestmark = pytest.mark.django_db
ORDER_DETAIL_URL = "order:order-detail"
ORDER_LIST_URL = "order:order-list"
ORDER_ITEM_DETAIL_URL = "order:orderitem-detail"
ORDER_ITEM_LIST_URL = "order:orderitem-list"
CREATE_ORDER_URL = "order:order-create-order-with-items"
SALES_REPORT_URL = "order:order-generate-sales-report"
CANCEL_ORDER_URL="order:order-cancel-order"
COMPLETE_ORDER_URL= "order:order-complete-order"
SET_PENDING_URL="order:order-set-pending"
MODIFY_ITEM_URL ="order:order-modify-item"
GENERATE_SALES_REPORT_URL="order:order-generate-sales-report"
from order.models import Order,OrderItem


class TestOrderEndpoints:

    def test_create_order(self, api_client, mocked_authentication):
        initiator = UserFactory(role='admin')
        product1 = ProductFactory(created_by=initiator)
        product2 = ProductFactory(created_by=initiator)
        product3 = ProductFactory(created_by=initiator)
        regular_user = UserFactory(role='regular_user')

        payload = {
            "items": [
                {
                    "product": product1.id,
                    "quantity_required": 4,
                },
                {"product": product2.id, "quantity_required": 6},
                {"product": product3.id, "quantity_required": 3},
            ]
        }

        mocked_authentication(active_user=regular_user)
        url = reverse(CREATE_ORDER_URL)
        response = api_client.post(url, data=payload, format="json")
        assert response.status_code == 200

    def test_deny_unathenticated_user_order_creation(self, api_client):
        initiator = UserFactory(role='admin')
        product1 = ProductFactory(created_by=initiator)
        product2 = ProductFactory(created_by=initiator)
        product3 = ProductFactory(created_by=initiator)

        payload = {
            "items": [
                {
                    "product": product1.id,
                    "quantity_required": 4,
                },
                {"product": product2.id, "quantity_required": 6},
                {"product": product3.id, "quantity_required": 3},
            ]
        }

        url = reverse(CREATE_ORDER_URL)
        response = api_client.post(url, data=payload, format="json")
        assert response.status_code == 401

    def test_list_orders(self, mocked_authentication, api_client):
        initiator = UserFactory(role='admin')
        product1 = ProductFactory(created_by=initiator)
        product2 = ProductFactory(created_by=initiator)
        regular_user1 = UserFactory(role='regular_user')
        regular_user2 = UserFactory(role='regular_user')

        order1 = OrderFactory(owner=regular_user1)
        order2 = OrderFactory(owner=regular_user2)
        order3 = OrderFactory(owner=regular_user1)

        OrderItemFactory.create_batch(4, product=product1, order=order1)
        OrderItemFactory.create_batch(3, product=product2, order=order2)
        OrderItemFactory.create_batch(3, product=product2, order=order3)

        mocked_authentication(active_user=regular_user1)

        url = reverse(ORDER_LIST_URL)
        response = api_client.get(url)
        print(response.data)
        assert response.status_code == 200
        assert Order.objects.count() == 3
        assert response.json()["total"] == 2

    def test_get_order(self, mocked_authentication, api_client):
        initiator = UserFactory(role='admin')
        product1 = ProductFactory(created_by=initiator)
        product2 = ProductFactory(created_by=initiator)
        regular_user1 = UserFactory(role='regular_user')
        order1 = OrderFactory(owner=regular_user1)
        OrderItemFactory( product=product1, order=order1)
        OrderItemFactory( product=product2, order=order1)

        mocked_authentication(active_user=regular_user1)
        url = reverse(ORDER_DETAIL_URL,kwargs={'pk':order1.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert Order.objects.count() == 1
        assert len(response.data["items"]) == 2

    def test_delete_order(
        self,
        mocked_authentication,
        api_client,
    ):
        """Test deleting of an order"""
        initiator = UserFactory(role='admin')
        product1 = ProductFactory(created_by=initiator)
        product2 = ProductFactory(created_by=initiator)
        regular_user1 = UserFactory(role='regular_user')
        order1 = OrderFactory(owner=regular_user1)
        OrderItemFactory(product=product1, order=order1)
        OrderItemFactory(product=product2, order=order1)

        mocked_authentication(active_user=regular_user1)
        url = reverse(ORDER_DETAIL_URL, kwargs={'pk': order1.id})
        response = api_client.delete(url)

        assert response.status_code == 204
        assert OrderItem.objects.count() == 0

    @pytest.mark.parametrize(
        "role, status_code",
        [
            ('admin', 200),
            ('regular_user', 403),
        ],
    )
    def test_cancel_order(self, mocked_authentication_with_role, api_client, status_code, role):
        """Test cancelling of an order"""
        initiator = UserFactory(role='admin')
        product1 = ProductFactory(created_by=initiator)
        product2 = ProductFactory(created_by=initiator)
        regular_user1 = UserFactory(role='regular_user')
        order1 = OrderFactory(owner=regular_user1,status='pending')
        OrderItemFactory(product=product1, order=order1)
        OrderItemFactory(product=product2, order=order1)

        mocked_authentication_with_role(active_user=regular_user1, role=role)
        url = reverse(CANCEL_ORDER_URL, kwargs={'pk': order1.id})
        response = api_client.post(url)

        assert response.status_code == status_code
        if status_code ==200 :

            assert Order.objects.count() == 1
            order1.refresh_from_db()
            assert order1.status=='cancelled'

    @pytest.mark.parametrize(
        "role, status_code",
        [
            ('admin', 200),
            ('regular_user', 403),
        ],
    )
    def test_complete_order(self, mocked_authentication_with_role, api_client, status_code, role):
        """Test complete of an order"""
        initiator = UserFactory(role='admin')
        product1 = ProductFactory(created_by=initiator)
        product2 = ProductFactory(created_by=initiator)
        regular_user1 = UserFactory(role='regular_user')
        order1 = OrderFactory(owner=regular_user1, status='pending')
        OrderItemFactory(product=product1, order=order1)
        OrderItemFactory(product=product2, order=order1)

        mocked_authentication_with_role(active_user=regular_user1, role=role)
        url = reverse(COMPLETE_ORDER_URL, kwargs={'pk': order1.id})
        response = api_client.post(url)

        assert response.status_code == status_code
        if status_code == 200:

            assert Order.objects.count() == 1
            order1.refresh_from_db()
            assert order1.status == 'completed'

    @pytest.mark.parametrize(
        "role, status_code",
        [
            ('admin', 200),
            ('regular_user', 403),
        ],
    )
    def test_set_pending_order(self, mocked_authentication_with_role, api_client, status_code, role):
        """Test pending of an order"""
        initiator = UserFactory(role='admin')
        product1 = ProductFactory(created_by=initiator)
        product2 = ProductFactory(created_by=initiator)
        regular_user1 = UserFactory(role='regular_user')
        order1 = OrderFactory(owner=regular_user1, status='cancelled')
        OrderItemFactory(product=product1, order=order1)
        OrderItemFactory(product=product2, order=order1)

        mocked_authentication_with_role(active_user=regular_user1, role=role)
        url = reverse(SET_PENDING_URL, kwargs={'pk': order1.id})
        response = api_client.post(url)

        assert response.status_code == status_code
        if status_code == 200:

            assert Order.objects.count() == 1
            order1.refresh_from_db()
            assert order1.status == 'pending'

    def test_modify_order_item(
        self,
        mocked_authentication,
        api_client,
    ):
        """Test modify of an  item in an order"""
        initiator = UserFactory(role='admin')
        product1 = ProductFactory(created_by=initiator)
        regular_user1 = UserFactory(role='regular_user')
        order = OrderFactory(owner=regular_user1)
        item=OrderItemFactory(product=product1,quantity_required=2, order=order)
        payload = {"product": product1.id, "quantity_required": 4}

        mocked_authentication(active_user=regular_user1)
        url = reverse(MODIFY_ITEM_URL, kwargs={'pk': order.id,"item_id":item.id})
        response = api_client.patch(url, data=payload, format="json")

        assert response.status_code == 200
        item.refresh_from_db()
        assert item.quantity_required == 4

    @pytest.mark.parametrize(
        "role, status_code",
        [
            ('admin', 200),
            ('regular_user', 403),
        ],
    )
    def test_generate_sales_report(self, mocked_authentication_with_role, api_client, status_code, role):
        """generate sales report by date range.."""
        initiator = UserFactory(role='admin')
        product1 = ProductFactory(
            created_by=initiator, price=3.00, 
        )
        product2 = ProductFactory(
            created_by=initiator, price=2.00, 
        )
      
        regular_user1 = UserFactory(role='regular_user')
        order = OrderFactory(owner=regular_user1)
        OrderItemFactory(product=product1, quantity_required=2, order=order)
        OrderItemFactory(product=product2, quantity_required=4, order=order)
        active_user=UserFactory()

        start_date = "2024-01-01T00:00:00.000000Z"
        end_date = "2024-12-31T23:59:59.999999Z"

        url = reverse(GENERATE_SALES_REPORT_URL)
        joined_url = f"{url}?start_date={start_date}&end_date={end_date}"
        mocked_authentication_with_role(active_user=active_user,role=role)
        response = api_client.post(joined_url,format="json")
        print(response)

        assert response.status_code == status_code
        if role == 'admin':
            assert 'data' in response.data
            assert 'total_sales_amount' in response.data
            
