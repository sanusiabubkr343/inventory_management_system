from django.urls import path, include
from .views import OrderViewSets
from rest_framework import routers

app_name = "order"
router = routers.DefaultRouter()

router.register("", viewset=OrderViewSets)

urlpatterns = [path("", include(router.urls))]
