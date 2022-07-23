from rest_framework.serializers import (
    ModelSerializer, SlugRelatedField,
    HiddenField, CurrentUserDefault
)

from carts.models import Cart, CartItem, Address
from products.models import Product


class AddressDetailSerializer(ModelSerializer):
    """Address serializer"""

    class Meta:
        model = Address
        fields = (
            'id',
            'title',
            'street',
            'city',
            'state',
            'zip_code',
            'country',
            'phone',
            'created',
            'modified'
        )


class AddressListSerializer(ModelSerializer):
    """Address serializer"""

    class Meta:
        model = Address
        fields = (
            'id',
            'title',
            'street',
            'zip_code',
            'phone'
        )


class AddressCreateUpdateSerializer(ModelSerializer):
    """Address serializer"""

    class Meta:
        model = Address
        fields = (
            'id',
            'title',
            'street',
            'city',
            'state',
            'zip_code',
            'country',
            'phone'
        )


class CartItemDetailSerializer(ModelSerializer):
    """Cart item serializer"""

    class Meta:
        model = CartItem
        fields = (
            'id',
            'product',
            'quantity',
            'total_price'
        )


class CartItemCreateUpdateSerializer(ModelSerializer):
    """Cart item serializer"""
    product = SlugRelatedField(slug_field='id', queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = (
            'id',
            'product',
            'quantity',
        )


class CartDetailSerializer(ModelSerializer):
    """Cart detail serializer"""
    address = AddressDetailSerializer(read_only=True)
    items = CartItemDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            'id',
            'step',
            'address',
            'items',
            'total_price',
            'created',
            'modified'
        )


class CartCreateUpdateSerializer(ModelSerializer):
    """Cart create update serializer"""
    address = SlugRelatedField(slug_field='id', queryset=Address.objects.all())
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Cart
        fields = (
            'id',
            'step',
            'user',
            'address',
            'created',
            'modified'
        )
