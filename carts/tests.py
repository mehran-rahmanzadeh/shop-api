from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse_lazy

from carts.models import Cart, CartItem, Address
from categories.models import Category
from products.models import Product


class TestCart(APITestCase):
    """Test cart
    model test
    api endpoints test
    """

    def setUp(self) -> None:
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
        self.address_title = 'Test Address'
        self.street = 'Test Street'
        self.city = 'Test City'
        self.state = 'Test State'
        self.country = 'Test Country'
        self.zip_code = '55555'
        self.phone = '+989059528767'
        self.address = self.create_address(
            title=self.address_title,
            street=self.street,
            city=self.city,
            state=self.state,
            country=self.country,
            zip_code=self.zip_code,
            phone=self.phone,
            user=self.user
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

    @staticmethod
    def create_address(title, street, city, state, country, zip_code, user, phone):
        """Create address"""
        return Address.objects.create(
            title=title,
            street=street,
            city=city,
            state=state,
            country=country,
            zip_code=zip_code,
            user=user,
            phone=phone
        )

    @staticmethod
    def generate_jwt_access_token_for_user(user):
        """Authenticate user and generate token"""
        return str(RefreshToken.for_user(user).access_token)

    def test_create_cart(self):
        """Test create cart"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)

    def test_create_cart_item(self):
        """Test create cart item"""
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=self.quantity
        )
        self.assertEqual(item.cart, self.cart)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, self.quantity)

    def test_cart_item_total_price_property(self):
        total = self.cart_item.product.final_price * self.cart_item.quantity
        self.assertEqual(self.cart_item.total_price, total)

    def test_cart_total_price_property(self):
        prices = [item.product.final_price * item.quantity for item in self.cart.items.all()]
        total = sum(prices)
        self.assertEqual(self.cart.total_price, total)

    def test_get_user_cart_authenticated(self):
        """Test get user cart authenticated"""
        token = self.generate_jwt_access_token_for_user(self.user)
        url = reverse_lazy('cart-current')
        response = self.client.get(url, {}, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total_price'], self.cart.total_price)

    def test_get_user_cart_unauthorized(self):
        """Test get user cart unauthorized"""
        url = reverse_lazy('cart-current')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_add_product_to_cart_authenticated(self):
        """Test add product to cart authenticated"""
        token = self.generate_jwt_access_token_for_user(self.user)
        url = reverse_lazy('cart-add-to-cart')
        payload = {
            'product': self.product.id,
            'quantity': 3
        }
        response = self.client.post(url, payload, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(self.cart.total_price, self.product.final_price * 3)

    def test_add_product_to_cart_unauthorized(self):
        """Test add product to cart unauthorized"""
        url = reverse_lazy('cart-add-to-cart')
        payload = {
            'product': self.product.id,
            'quantity': 3
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 401)

    def test_update_cart_item_authenticated(self):
        """Test update cart item authenticated"""
        token = self.generate_jwt_access_token_for_user(self.user)
        url = reverse_lazy('cart-update-item')
        payload = {
            'product': self.product.id,
            'quantity': 4
        }
        response = self.client.patch(url, payload, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(self.cart.total_price, self.product.final_price * 4)

    def test_update_cart_item_unauthorized(self):
        """Test update cart item unauthorized"""
        url = reverse_lazy('cart-update-item')
        payload = {
            'product': self.product.id,
            'quantity': 3
        }
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, 401)

    def test_delete_cart_item_authenticated(self):
        """Test delete cart item authenticated"""
        token = self.generate_jwt_access_token_for_user(self.user)
        url = reverse_lazy('cart-delete-item')
        payload = {
            'product': self.product.id
        }
        response = self.client.delete(url, payload, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(self.cart.total_price, 0)

    def test_delete_cart_item_unauthorized(self):
        """Test delete cart item unauthorized"""
        url = reverse_lazy('cart-delete-item')
        payload = {
            'product': self.product.id
        }
        response = self.client.delete(url, payload)
        self.assertEqual(response.status_code, 401)

    def test_add_address_to_cart_authenticated(self):
        """Test add address to cart authenticated"""
        token = self.generate_jwt_access_token_for_user(self.user)
        url = reverse_lazy('cart-update-address')
        payload = {
            'address': self.address.id
        }
        response = self.client.patch(url, payload, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data['address']['title'], self.address.title)
        self.assertEqual(response.data['address']['street'], self.address.street)
        self.assertEqual(response.data['address']['city'], self.address.city)
        self.assertEqual(response.data['address']['country'], self.address.country)
        self.assertEqual(response.data['address']['zip_code'], self.address.zip_code)
        self.assertEqual(response.data['address']['phone'], self.address.phone)

    def test_add_address_to_cart_unauthorized(self):
        """Test add address to cart unauthorized"""
        url = reverse_lazy('cart-update-address')
        payload = {
            'address': self.address.id
        }
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, 401)

    def test_get_user_address_list_authenticated(self):
        """Test get user address list authenticated"""
        token = self.generate_jwt_access_token_for_user(self.user)
        url = reverse_lazy('address-list')
        response = self.client.get(url, {}, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_user_address_list_unauthorized(self):
        """Test get user address list unauthorized"""
        url = reverse_lazy('address-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_delete_user_address_authenticated(self):
        token = self.generate_jwt_access_token_for_user(self.user)
        url = reverse_lazy('address-detail', kwargs={'id': self.address.id})
        response = self.client.delete(url, {}, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)

    def test_delete_user_address_unauthorized(self):
        url = reverse_lazy('address-detail', kwargs={'id': self.address.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_create_user_address_authenticated(self):
        token = self.generate_jwt_access_token_for_user(self.user)
        payload = {
            'title': 'Test address',
            'street': 'Test street',
            'city': 'Test city',
            'state': 'Test state',
            'country': 'Test country',
            'zip_code': '44444',
            'phone': '+991234567890'
        }
        url = reverse_lazy('address-list')
        response = self.client.post(url, payload, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['street'], payload['street'])
        self.assertEqual(response.data['city'], payload['city'])
        self.assertEqual(response.data['state'], payload['state'])
        self.assertEqual(response.data['country'], payload['country'])
        self.assertEqual(response.data['zip_code'], payload['zip_code'])
        self.assertEqual(response.data['phone'], payload['phone'])

    def test_create_user_address_invalid_zipcode(self):
        """Test create user address invalid zipcode"""
        token = self.generate_jwt_access_token_for_user(self.user)
        payload = {
            'title': 'Test address',
            'street': 'Test street',
            'city': 'Test city',
            'state': 'Test state',
            'country': 'Test country',
            'zip_code': '4444',
            'phone': '+991234567890'
        }
        url = reverse_lazy('address-list')
        response = self.client.post(url, payload, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 400)

    def test_create_user_address_invalid_phone(self):
        """Test create user address invalid phone"""
        token = self.generate_jwt_access_token_for_user(self.user)
        payload = {
            'title': 'Test address',
            'street': 'Test street',
            'city': 'Test city',
            'state': 'Test state',
            'country': 'Test country',
            'zip_code': '44444',
            'phone': '+99123456'
        }
        url = reverse_lazy('address-list')
        response = self.client.post(url, payload, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 400)

    def test_create_user_address_unauthorized(self):
        payload = {
            'title': 'Test address',
            'street': 'Test street',
            'city': 'Test city',
            'state': 'Test state',
            'country': 'Test country',
            'zip_code': '44444',
            'phone': '+991234567890'
        }
        url = reverse_lazy('address-list')
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 401)

    def test_get_user_address_detail_authenticated(self):
        token = self.generate_jwt_access_token_for_user(self.user)
        url = reverse_lazy('address-detail', kwargs={'id': self.address.id})
        response = self.client.get(url, {}, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.address.title)
        self.assertEqual(response.data['street'], self.address.street)
        self.assertEqual(response.data['city'], self.address.city)
        self.assertEqual(response.data['state'], self.address.state)
        self.assertEqual(response.data['country'], self.address.country)
        self.assertEqual(response.data['zip_code'], self.address.zip_code)
        self.assertEqual(response.data['phone'], self.address.phone)

    def test_get_user_address_detail_unauthorized(self):
        url = reverse_lazy('address-detail', kwargs={'id': self.address.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_update_user_address_authenticated(self):
        """Test update user address authenticated"""
        token = self.generate_jwt_access_token_for_user(self.user)
        payload = {
            'title': 'Test address 2',
            'street': 'Test street 2',
            'city': 'Test city 2',
            'state': 'Test state 2',
            'country': 'Test country 2',
            'zip_code': '44442',
            'phone': '+991234567892'
        }
        url = reverse_lazy('address-detail', kwargs={'id': self.address.id})
        response = self.client.patch(url, payload, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['street'], payload['street'])
        self.assertEqual(response.data['city'], payload['city'])
        self.assertEqual(response.data['state'], payload['state'])
        self.assertEqual(response.data['country'], payload['country'])
        self.assertEqual(response.data['zip_code'], payload['zip_code'])
        self.assertEqual(response.data['phone'], payload['phone'])

    def test_update_user_address_invalid_zipcode(self):
        """Test update user address invalid zipcode"""
        token = self.generate_jwt_access_token_for_user(self.user)
        payload = {
            'title': 'Test address',
            'street': 'Test street',
            'city': 'Test city',
            'state': 'Test state',
            'country': 'Test country',
            'zip_code': '4444',
            'phone': '+991234567890'
        }
        url = reverse_lazy('address-detail', kwargs={'id': self.address.id})
        response = self.client.patch(url, payload, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 400)

    def test_update_user_address_invalid_phone(self):
        """Test update user address invalid phone"""
        token = self.generate_jwt_access_token_for_user(self.user)
        payload = {
            'title': 'Test address',
            'street': 'Test street',
            'city': 'Test city',
            'state': 'Test state',
            'country': 'Test country',
            'zip_code': '44444',
            'phone': '+99123456'
        }
        url = reverse_lazy('address-detail', kwargs={'id': self.address.id})
        response = self.client.patch(url, payload, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 400)

    def test_update_user_address_unauthorized(self):
        """Test update user address unauthorized"""
        payload = {
            'title': 'Test address',
            'street': 'Test street',
            'city': 'Test city',
            'state': 'Test state',
            'country': 'Test country',
            'zip_code': '44444',
            'phone': '+991234567890'
        }
        url = reverse_lazy('address-detail', kwargs={'id': self.address.id})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, 401)
