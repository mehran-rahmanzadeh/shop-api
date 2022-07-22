from django_filters import FilterSet
from mptt.fields import TreeNodeChoiceField

from categories.models import Category


class CategoryFilter(FilterSet):
    """Category filter class
    filter category tree by parent
    """
    parent = TreeNodeChoiceField(
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = Category
        fields = (
            'parent',
        )
        order_by = 'order'
