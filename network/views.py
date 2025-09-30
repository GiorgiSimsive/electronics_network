from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import NetworkUnit, Product
from .serializers import NetworkUnitSerializer, ProductSerializer


class NetworkUnitViewSet(viewsets.ModelViewSet):
    """
    CRUD для «поставщика» (в терминах задания — это звено сети).
    Добавлен фильтр по стране: /api/suppliers/?country=Georgia
    """
    queryset = NetworkUnit.objects.select_related("supplier").prefetch_related("products").all()
    serializer_class = NetworkUnitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]


class ProductViewSet(viewsets.ModelViewSet):
    """
    Небольшой CRUD для продуктов, чтобы можно было создавать/привязывать их.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
