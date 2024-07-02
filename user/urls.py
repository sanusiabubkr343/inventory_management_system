from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers


from . import views

app_name = "user"
router = routers.DefaultRouter()

router.register("", viewset=views.UserViewSets)


urlpatterns = [
    path("users/", include(router.urls)),
    path("users/jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
   
]
