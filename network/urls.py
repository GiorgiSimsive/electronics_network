from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NetworkUnitViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"suppliers", NetworkUnitViewSet, basename="suppliers")
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]
