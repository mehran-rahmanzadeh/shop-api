from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields

from products.models import Product


@registry.register_document
class ProductDocument(Document):
    """Product document mapping."""
    category = fields.TextField()

    def prepare_category(self, instance):
        return instance.category.title if instance.category else None

    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Product
        fields = (
            'title',
            'slug',
            'final_price',
        )

    def get_queryset(self):
        return super().get_queryset().select_related('category')
