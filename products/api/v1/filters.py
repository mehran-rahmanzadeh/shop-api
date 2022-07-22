from django_filters import FilterSet, NumberFilter

from categories.models import Category
from products.models import Product


def filter_category_children_products(queryset, field, value, **kwargs):
    """Filter products by category children"""
    if not value:
        return queryset

    cat = Category.objects.filter(id=value)
    if cat.exists():
        cat = cat.first()
        cat_children_id_list = cat.get_descendants(include_self=True).values_list('id', flat=True)
        qs = queryset.filter(category__id__in=cat_children_id_list)
    else:
        qs = Product.objects.none()

    return qs


class ProductFilter(FilterSet):
    """Product filter class"""
    category = NumberFilter(method=filter_category_children_products)

    class Meta:
        model = Product
        fields = (
            'category',
        )
