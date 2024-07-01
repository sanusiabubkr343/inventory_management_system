from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import routers

from . import views

app_name = "user"
router = routers.DefaultRouter()

router.register("", viewset=views.UserViewSets)


urlpatterns = [
    path("users/", include(router.urls)),
    path("users/jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
