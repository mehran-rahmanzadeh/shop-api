from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from products.api.v1.filters import ProductFilter
from products.api.v1.serializers import ProductSerializer
from products.models import Product


class ProductViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Product viewset"""
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilter
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.select_related('category')
