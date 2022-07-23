from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from carts.api.v1.serializers import CartCreateUpdateSerializer, CartDetailSerializer, CartItemCreateUpdateSerializer
from carts.api.v1.utils import CartHelper


class CartViewSet(UpdateModelMixin, ListModelMixin, GenericViewSet):
    """Cart viewset"""
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'update':
            return CartCreateUpdateSerializer
        return CartDetailSerializer

    def get_queryset(self):
        return self.request.user.carts.all()

    @action(detail=False, methods=['get'])
    def current(self, *args, **kwargs):
        """Get current cart"""
        cart = CartHelper.get_current_cart(self.request.user)
        if cart:
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def add_to_cart(self, *args, **kwargs):
        """Add product to cart"""
        serializer = CartItemCreateUpdateSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        cart = CartHelper.get_current_cart(self.request.user)
        if cart:
            cart.add_product(product, quantity)
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'])
    def update_item(self, *args, **kwargs):
        """Update cart item"""
        serializer = CartItemCreateUpdateSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        cart = CartHelper.get_current_cart(self.request.user)
        if cart:
            cart.update_product(product, quantity)
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def delete_item(self, *args, **kwargs):
        """Delete cart item"""
        serializer = CartItemCreateUpdateSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        cart = CartHelper.get_current_cart(self.request.user)
        if cart:
            cart.delete_product(product)
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)
