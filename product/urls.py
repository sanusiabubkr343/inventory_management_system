from django.urls import path,include
from .views import ProductViewSets
from rest_framework import routers

app_name = "product"
router = routers.DefaultRouter()

router.register("",viewset=ProductViewSets)

url_patterns = [
  path("",include(router.urls))
]
