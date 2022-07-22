from rest_framework.serializers import ModelSerializer

from categories.api.v1.serializers import CategoryListSerializer
from products.models import Product


class ProductSerializer(ModelSerializer):
    """Product serializer"""
    category = CategoryListSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'slug',
            'title', 'category',
            'base_price', 'discount_amount',
            'discount_percentage', 'final_price',
            'has_discount', 'quantity',
            'description', 'image',
        )
