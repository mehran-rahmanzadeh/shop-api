from django.core.handlers.wsgi import WSGIRequest
from django.db import IntegrityError, transaction
from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from categories.models import Category
from products.models import Product


class TestProducts(APITestCase):
    """Test products
    model test
    api endpoints test
    """

    def setUp(self) -> None:
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

    def assert_product_fields(self, data, product):
        """Assert product fields
        :param response: rest client response
        :param product: product
        """
        self.assertEqual(data['title'], product.title)
        self.assertEqual(data['slug'], product.slug)
        self.assertEqual(data['description'], product.description)
        self.assertEqual(float(data['base_price']), product.base_price)
        self.assertEqual(float(data['discount_amount']), product.discount_amount)
        self.assertEqual(data['has_discount'], product.has_discount)
        self.assertEqual(int(data['quantity']), product.quantity)
        self.assertEqual(data['category']['title'], product.category.title)
        self.assertEqual(data['category']['slug'], product.category.slug)
        self.assertEqual(data['category']['description'], product.category.description)
        self.assertEqual(data['category']['order'], product.category.order)
        self.assertEqual(data['category']['image'], product.category.image)

    def test_create_product_success(self):
        """Test create product"""
        title = 'Test Product 2'
        slug = 'test-product-2'
        description = 'Test Product Description 2'
        base_price = 10.00
        discount_amount = 5.00
        has_discount = True
        quantity = 10
        product = self.create_product(
            title=title,
            description=description,
            base_price=base_price,
            discount_amount=discount_amount,
            has_discount=has_discount,
            quantity=quantity,
            category=self.category,
            slug=slug
        )
        self.assertEqual(product.title, title)
        self.assertEqual(product.slug, slug)
        self.assertEqual(product.description, description)
        self.assertEqual(product.base_price, base_price)
        self.assertEqual(product.discount_amount, discount_amount)
        self.assertEqual(product.has_discount, has_discount)
        self.assertEqual(product.quantity, quantity)
        self.assertEqual(product.category, self.category)

    def test_create_product_slug_duplicated(self):
        """Test create product with slug duplicated"""
        title = 'Test Product 2'
        description = 'Test Product Description 2'
        base_price = 10.00
        discount_amount = 5.00
        has_discount = True
        quantity = 10
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                _ = self.create_product(
                    title=title,
                    description=description,
                    base_price=base_price,
                    discount_amount=discount_amount,
                    has_discount=has_discount,
                    quantity=quantity,
                    category=self.category,
                    slug=self.slug
                )

        self.assertEqual(Product.objects.count(), 1)

    def test_product_final_price_property(self):
        """Test product final price property"""
        self.product.discount_amount = 0
        self.assertEqual(self.product.final_price, self.base_price)
        self.product.discount_amount = 10
        self.assertEqual(self.product.final_price, self.base_price - 10)
        self.product.has_discount = False
        self.assertEqual(self.product.final_price, self.base_price)

    def test_product_discount_percentage_property(self):
        """Test product discount percentage property"""
        self.product.discount_amount = 0
        self.assertEqual(self.product.discount_percentage, 0)
        self.product.discount_amount = 10
        self.assertEqual(self.product.discount_percentage, 10)
        self.product.has_discount = False
        self.assertEqual(self.product.discount_percentage, 0)

    def test_get_product_list(self):
        """Test get product list"""
        url = reverse_lazy('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assert_product_fields(response.data['results'][0], self.product)

    def test_retrieve_product(self):
        """Test retrieve product"""
        url = reverse_lazy('product-detail', kwargs={'slug': self.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assert_product_fields(response.data, self.product)

    def test_filter_product_by_category(self):
        """Test filter product by category"""
        url = reverse_lazy('product-list')
        url += '?category={}'.format(self.category.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assert_product_fields(response.data['results'][0], self.product)

    def test_filter_product_by_parent_category(self):
        """Test filter product by parent category"""
        child_category = self.create_category(
            title='Test category 2',
            slug='test-category-2', order=2,
            parent=self.category,
            description='Test description 2',
            image=None
        )
        child_product = self.create_product(
            title='Test product 2',
            slug='test-product-2',
            category=child_category,
            quantity=10,
            base_price=100,
            discount_amount=0,
            has_discount=False,
            description='Test description 2'
        )
        url = reverse_lazy('product-list')
        url += '?category={}'.format(self.category.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
