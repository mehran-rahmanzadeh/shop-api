from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from categories.api.v1.filters import CategoryFilter
from categories.api.v1.serializers import CategorySerializer
from categories.models import Category


class CategoryViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """Category viewset class"""
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CategoryFilter

    def get_queryset(self):
        return Category.objects.prefetch_related('children')
