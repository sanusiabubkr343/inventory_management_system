# test create product(200,401,403)
# test update,partial update(200,400,403)
# test delete(200,403)
# test list and get (200,401)

import pytest
from django.urls import reverse
from rest_framework import status
from user.test.factories import UserFactory

pytestmark = pytest.mark.django_db
PRODUCT_DETAIL_URL = "product:product-detail"
PRODUCT_LIST_URL = "product:product-list"


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
        "name,description,quantity,price", [('name1', "descr", 0, 2.4), ('name2',44, 0, 2.4),('name1',"descr",0,-2.4)]
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
        print(response)
        assert response.status_code == 400
