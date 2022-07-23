from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from carts.api.v1.utils import CartHelper
from discounts.api.v1.serializers import ValidateDiscountCodeSerializer
from discounts.api.v1.utils import DiscountCodeHelper


class ApplyDiscountCodeAPIView(APIView):
    """Apply discount code to cart"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ValidateDiscountCodeSerializer

    def post(self, *args, **kwargs):
        """Apply discount code to cart"""
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        if not DiscountCodeHelper.is_code_valid(code=code):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if DiscountCodeHelper.is_used_by_user(code=code, user=self.request.user):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cart = CartHelper.get_current_cart(user=self.request.user)
        DiscountCodeHelper.apply_discount_code_on_cart(code=code, cart=cart)
        return Response(status=status.HTTP_200_OK)
