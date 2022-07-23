from django.contrib.auth import get_user_model

from carts.models import Cart
from discounts.models import DiscountCode


class DiscountCodeHelper:
    def __init__(self, *args, **kwargs):
        super(DiscountCodeHelper, self).__init__(*args, **kwargs)

    @staticmethod
    def __get_discount_code_obj(code):
        return DiscountCode.objects.get(code=code)

    @classmethod
    def is_code_valid(cls, code: str):
        """Check if code is valid"""
        return DiscountCode.objects.filter(code=code, is_active=True).exists()

    @classmethod
    def is_used_by_user(cls, code: str, user: get_user_model()):
        """Check if code is used by user"""
        if not cls.is_code_valid(code=code):
            raise ValueError('Code is not valid')
        discount_code = cls.__get_discount_code_obj(code=code)
        return discount_code.used_by.filter(id=user.id).exists()

    @classmethod
    def apply_discount_code_on_cart(cls, code: str, cart: Cart):
        """Set discount code to user cart"""
        if not cls.is_code_valid(code=code):
            raise ValueError('Code is not valid')
        if cls.is_used_by_user(code=code, user=cart.user):
            raise ValueError('Code is already used')
        discount_code = cls.__get_discount_code_obj(code=code)
        cart.discount_code = discount_code
        cart.save()
