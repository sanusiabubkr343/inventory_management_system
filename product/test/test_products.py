import pytest
from django.urls import reverse
from rest_framework import status
from user.test.factories import UserFactory
from product.test.factories import ProductFactory
pytestmark = pytest.mark.django_db
PRODUCT_DETAIL_URL = "product:product-detail"
PRODUCT_LIST_URL = "product:product-list"
STOCK_REPORT_URL = "product:product-generate-low-stock-report"


class TestProductEndpoints:
    @pytest.mark.parametrize(
        "role,status_code", [('admin', 201), ('regular_user', 403)]
    )
    def test_create_product(self, api_client,role,status_code,mocked_authentication_with_role):
        """Test creation of product"""
        user = UserFactory()
        mocked_authentication_with_role(active_user=user,role=role)
        payload = {
            "name": "ProductA",
            "description": "product description",
            "quantity": 2,
            "price":3.90
        }
        url = reverse(PRODUCT_LIST_URL)
        response = api_client.post(url, payload)

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "name,description,quantity,price", [('name1', 'descr', 0, 2.4), ('name2',4, 0, 2.4),('name3','descr',0,-2.4)]
    )
    def test_deny_creation_of_product_with_wrong_data(self, api_client, mocked_authentication_with_role,name,description,quantity,price):
        """Test deny  creation of task"""
        user = UserFactory()
        mocked_authentication_with_role(active_user=user, role='admin')
        payload = {
            "name": name,
            "description": description,
            "quantity": quantity,
            "price": price,
        }
        url = reverse(PRODUCT_LIST_URL)
        response = api_client.post(url, payload)
        assert response.status_code == 400

    def test_list_product(self, mocked_authentication, api_client):
        """Test  get list of products"""
        user = UserFactory()
        auth_user = mocked_authentication(active_user=user)
        ProductFactory.create_batch(3, created_by=auth_user)
        url = reverse(PRODUCT_LIST_URL)
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json()["total"] == 3

    def test_unauthorized_list_product(self, api_client):
        """Test unauthorized get list of  product"""
        user = UserFactory()
        ProductFactory.create_batch(3, created_by=user)
        url = reverse(PRODUCT_LIST_URL)
        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_product(self, mocked_authentication, api_client):
        """Test getting of a product"""
        user = UserFactory()
        auth_user = mocked_authentication(active_user=user)
        task = ProductFactory.create(created_by=auth_user)
        url = reverse(PRODUCT_DETAIL_URL, kwargs={"pk": task.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["name"] == task.name
        assert response.data["description"] == task.description

    def test_unauthorized_get_task(self, api_client):
        """Test unauthorized getting of a task"""
        user = UserFactory()
        task = ProductFactory.create(created_by=user)
        url = reverse(PRODUCT_DETAIL_URL, kwargs={"pk": task.id})
        response = api_client.get(url)
        assert response.status_code == 401

    @pytest.mark.parametrize(
    "method_name, role, status_code",
    [
        ('patch', 'admin', 200),
        ('put', 'admin', 200),
        ('patch', 'regular_user', 403),
        ('put', 'regular_user', 403),
        ('patch','', 403),
        ('put','', 403),
    ],
)
    def test_update_product(self,method_name, role, status_code, api_client, mocked_authentication_with_role):
        """Test updating a product"""
        user = UserFactory()
        auth_user = mocked_authentication_with_role(active_user=user, role=role)
        product = ProductFactory.create(name="old_products_name", created_by=auth_user)
        payload = {
        "name": "new_name",
        "description": "new description",
        "quantity": 3,
        "price": 4.09
         }
        url = reverse(PRODUCT_DETAIL_URL, kwargs={"pk": product.id})
        response = getattr(api_client, method_name)(url, data=payload)
        product.refresh_from_db()

        assert response.status_code == status_code
        if response.status_code == 200:
            assert response.data['name'] == payload['name']
            assert product.description == payload['description']

    @pytest.mark.parametrize(
        "role, status_code",
        [
            ('admin', 204),
            ('regular_user', 403),
        ],
    )
    def test_delete_product(self, mocked_authentication_with_role, api_client, status_code,role):
        """Test deleting of a product"""
        user = UserFactory()
        auth_user = mocked_authentication_with_role(active_user=user,role=role)
        task = ProductFactory.create(created_by=auth_user)
        url = reverse(PRODUCT_DETAIL_URL, kwargs={"pk": task.id})
        response = api_client.delete(url)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "role, status_code",
        [
            ('admin', 200),
            ('regular_user', 403),
        ],
    )
    def test_generate_low_stock_report(self, api_client, role, status_code, mocked_authentication_with_role):
        """test endpoint for generating a report of all products that are low in stock with respect to input qunatity,e,g report with quantity less than 10"""
        user1 = UserFactory()
        user2=UserFactory()
        ProductFactory(quantity=5,created_by=user1)
        ProductFactory(quantity=6, created_by=user1)
        ProductFactory(quantity=3, created_by=user2)
        ProductFactory(quantity=9, created_by=user2)
        mocked_authentication_with_role(active_user=user1, role=role)
        quantity_threshold=7
        url = reverse(STOCK_REPORT_URL)
        joined_url = url + f"?quantity={quantity_threshold}"
        response = api_client.post(joined_url,format="json")
    
        assert response.status_code == status_code
        if response.status_code == 200:
           assert response.json().get("total") == 3
