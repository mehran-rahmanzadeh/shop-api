from rest_framework import serializers
from discounts.models import DiscountCode


class ValidateDiscountCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
