from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from elasticsearch_dsl import Q

from products.api.v1.serializers import ProductSerializer
from products.models import Product
from search.api.v1.filters import CustomSearchBackend
from search.api.v1.serializers import ProductDocumentSerializer
from search.documents import ProductDocument


class ProductElasticsearchViewSet(APIView, LimitOffsetPagination):
    """Product elasticsearch viewset"""
    serializer_class = ProductDocumentSerializer
    document_class = ProductDocument

    @staticmethod
    def generate_elasticsearch_query_expression(query):
        """Generate elasticsearch query expression."""
        if query:
            return Q('multi_match', query=query, fields=['title', 'slug', 'category'])
        return Q('match_all')

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        query_expression = self.generate_elasticsearch_query_expression(query)
        documents = self.document_class.search().query(query_expression)
        paginated_documents = self.paginate_queryset(documents, request=request, view=self)
        serializer = self.serializer_class(paginated_documents, many=True)
        return self.get_paginated_response(serializer.data)


class ProductPostgresTrigramSearchViewset(ListModelMixin, GenericViewSet):
    """Product postgres trigram search viewset"""
    serializer_class = ProductSerializer
    filter_backends = [CustomSearchBackend]
    search_fields = ('title', 'slug', 'category__name')
    search_type = 'trigram'  # can be one of the vector, rank, trigram

    def get_queryset(self):
        return self.filter_queryset(Product.objects.select_related('category'))

