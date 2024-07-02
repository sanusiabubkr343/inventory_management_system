import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.authentication import JWTAuthentication


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def mocked_authentication(mocker):

    def _user(active_user=None, is_active=True):
        if active_user:
            active_user.is_active=is_active
            active_user.save()
            active_user.refresh_from_db()
        mocked_user_data = active_user
        mocker.patch.object(JWTAuthentication,"authenticate",return_value=(active_user,None))
        return mocked_user_data
    return _user


@pytest.fixture
def mocked_authentication_with_role(mocker):

    def _user(active_user=None, is_active=True,role=None):
        
        active_user.is_active = is_active
        active_user.role=role
        active_user.save()
        active_user.refresh_from_db()
        mocked_user_data = active_user
        mocker.patch.object(JWTAuthentication, "authenticate", return_value=(active_user, None))
        return mocked_user_data

    return _user
