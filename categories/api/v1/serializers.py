from rest_framework.serializers import ModelSerializer

from categories.models import Category


class CategorySerializer(ModelSerializer):
    """Category serializer class"""

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'order',
            'image'
        )

    def get_fields(self):
        fields = super().get_fields()
        fields['children'] = CategorySerializer(many=True, required=False)
        return fields


class CategoryListSerializer(ModelSerializer):
    """Category serializer class"""

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'order',
            'image'
        )
