from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from search.documents import ProductDocument


class ProductDocumentSerializer(DocumentSerializer):
    """Product document serializer."""

    class Meta:
        document = ProductDocument
        fields = (
            'id',
            'title',
            'slug',
            'category',
            'final_price',
            'image',
        )
