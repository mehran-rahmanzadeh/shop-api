from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

from carts.models import CartItem, Cart
from categories.models import Category
from discounts.models import DiscountCode
from products.models import Product


class TestDiscountCode(APITestCase):
    """Test discount code
    model test
    api endpoint test
    """
    def setUp(self):
        self.percent_code = 'test2022'
        self.kind = 'percent'
        self.fixed_percentage = 20
        self.amount = None
        self.is_active = True
        self.percent_discount = self.create_discount_code(
            code=self.percent_code,
            kind=self.kind,
            percentage=self.fixed_percentage,
            amount=self.amount,
            is_active=self.is_active
        )
        self.fixed_code = 'test2023'
        self.kind = 'amount'
        self.percentage = None
        self.fixed_amount = 100
        self.is_active = True
        self.fixed_discount = self.create_discount_code(
            code=self.fixed_code,
            kind=self.kind,
            percentage=self.percentage,
            amount=self.fixed_amount,
            is_active=self.is_active
        )
        self.username = 'test_user'
        self.password = 'secure_password'
        self.user = self.create_user(self.username, self.password)
        self.cart = self.create_cart(self.user)
        self.title = 'Test Product'
        self.slug = 'test-product'
        self.description = 'Test Product Description'
        self.base_price = 100.00
        self.discount_amount = 5.00
        self.has_discount = True
        self.quantity = 10
        self.category_title = 'Test Category'
        self.category_description = 'Test Category Description'
        self.category_slug = 'test-category'
        self.category_parent = None
        self.category_order = 1
        self.category_image = None
        self.category = self.create_category(
            title=self.category_title,
            description=self.category_description,
            slug=self.category_slug,
            parent=self.category_parent,
            order=self.category_order,
            image=self.category_image
        )
        self.product = self.create_product(
            title=self.title,
            description=self.description,
            base_price=self.base_price,
            discount_amount=self.discount_amount,
            has_discount=self.has_discount,
            quantity=self.quantity,
            category=self.category,
            slug=self.slug
        )
        self.quantity = 2
        self.cart_item = self.create_cart_item(self.cart, self.product, self.quantity)

    @staticmethod
    def create_discount_code(code, kind, percentage, amount, is_active):
        """Create discount code"""
        return DiscountCode.objects.create(
            code=code,
            kind=kind,
            percentage=percentage,
            amount=amount,
            is_active=is_active
        )

    @staticmethod
    def create_user(username, password):
        return get_user_model().objects.create_user(
            username=username,
            password=password
        )

    @staticmethod
    def create_cart(user):
        return Cart.objects.create(user=user)

    @staticmethod
    def create_cart_item(cart, product, quantity):
        return CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )

    @staticmethod
    def create_product(title, slug, base_price, discount_amount, has_discount, quantity, category, description):
        """Create product"""
        return Product.objects.create(
            title=title,
            slug=slug,
            base_price=base_price,
            discount_amount=discount_amount,
            category=category,
            description=description,
            has_discount=has_discount,
            quantity=quantity
        )

    @staticmethod
    def create_category(title, slug, description, parent, order, image):
        """Create category"""
        return Category.objects.create(
            title=title,
            slug=slug,
            description=description,
            parent=parent,
            order=order,
            image=image
        )

    def test_create_discount_code(self):
        """Test create discount code"""
        self.assertEqual(self.percent_discount.code, self.percent_code)
        self.assertEqual(self.percent_discount.kind, 'percent')
        self.assertEqual(self.percent_discount.percentage, self.fixed_percentage)
        self.assertEqual(self.percent_discount.amount, self.amount)
        self.assertEqual(self.percent_discount.is_active, self.is_active)
        self.assertEqual(self.fixed_discount.code, self.fixed_code)
        self.assertEqual(self.fixed_discount.kind, 'amount')
        self.assertEqual(self.fixed_discount.percentage, self.percentage)
        self.assertEqual(self.fixed_discount.amount, self.fixed_amount)
        self.assertEqual(self.fixed_discount.is_active, self.is_active)

    def test_create_discount_code_duplicate_failure(self):
        """Test create discount code duplicate failure"""
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_discount_code(
                    code=self.percent_code,
                    kind=self.kind,
                    percentage=self.fixed_percentage,
                    amount=self.amount,
                    is_active=self.is_active
                )

        self.assertEqual(DiscountCode.objects.count(), 2)
