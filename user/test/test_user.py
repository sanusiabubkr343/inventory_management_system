import pytest
from django.urls import reverse
from rest_framework import status
from .factories import UserFactory

pytestmark = pytest.mark.django_db
LOGIN_URL = "user:user-login"
REGISTER_URL = "user:user-register-user"


class TestUserEndpoints:

    @pytest.mark.parametrize(
        "email,role", [('user@example.com', 'regular_user'), ('admin@example.com', 'admin')]
    )
    def test_user_registration(self, api_client,email, role):
        """test user registration with correct credentials"""
        payload = {
            "email": email,
            "password": "stringst",
            "firstname": "string",
            "lastname": "string",
            "role": role,
        }
        url = reverse(REGISTER_URL)

        response = api_client.post(url, data=payload)
        assert response.status_code == 201
        assert response.json()["data"]["is_active"] is True
        assert response.json()["data"]["id"] is not None

    @pytest.mark.parametrize(
        "email,role", [('user@example.1.com', 'regular-user'), ('admin@example.gm.com', 'Admin')]
    )
    def test_deny_user_registration(self, api_client, email, role):
        """test deny registration with wrong data"""
        payload = {
            "email": email,
            "password": "stringst",
            "firstname": "string",
            "lastname": "string",
            "role": role,
        }
        url = reverse(REGISTER_URL)
        response = api_client.post(url, data=payload)
        assert response.status_code == 400

    def test_user_login(self, api_client):
        user = UserFactory(email="sanusi@gmail.com",password="password123",is_active=True)
        user.refresh_from_db()
        payload = {
            "email":user.email,
            "password":"password123" #user.password is already hashed/encrypted
        }
        print(payload)

        url = reverse(LOGIN_URL)
        response = api_client.post(url, data=payload)

        assert response.status_code == 200
        assert "access" in response.json()["data"]["tokens"]
        assert "refresh" in response.json()["data"]["tokens"]

    def test_deny_user_login(self, api_client):
        """test deny login with wrong credentials"""
        user = UserFactory(email="sanusi@gmail.com", password="password123", is_active=True)
        payload = {"email":user.email, "password": "wrongPassword"}
        url = reverse("user:user-login")
        response = api_client.post(url, data=payload)
        assert response.status_code == 401
