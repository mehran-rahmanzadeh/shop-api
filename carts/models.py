from django.db import models
from django.conf import settings
from django.db.models import Sum, F
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from painless.utils.models.mixins import TimeStampModelMixin


class Address(TimeStampModelMixin):
    """
    Address model
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='addresses'
    )
    title = models.CharField(
        _('Title'),
        max_length=255,
        null=True,
        blank=True
    )
    street = models.CharField(
        _('Street'),
        max_length=255
    )
    city = models.CharField(
        _('City'),
        max_length=255
    )
    state = models.CharField(
        _('State'),
        max_length=255
    )
    zip_code = models.CharField(
        _('Zip code'),
        max_length=5,
        validators=[RegexValidator(r'^[0-9]{5}(?:-[0-9]{4})?$')]
    )
    country = models.CharField(
        _('Country'),
        max_length=255
    )
    phone = models.CharField(
        _('Phone'),
        max_length=15,
        null=True,
        blank=True,
        validators=[RegexValidator(r'^(\+\d{1,3})?,?\s?\d{8,13}')]
    )

    def __str__(self):
        return self.street

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        ordering = ('-created',)


class Cart(TimeStampModelMixin):
    """
    Cart model
    """
    STEP_CHOICES = (
        ('initial', _('Initial')),
        ('pending', _('Pending')),
        ('paid', _('Paid'))
    )
    step = models.CharField(
        _('Step'),
        choices=STEP_CHOICES,
        max_length=20,
        default='initial'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='carts'
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Address')
    )
    discount_code = models.ForeignKey(
        'discounts.DiscountCode',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Discount code')
    )

    def __str__(self):
        return '{}'.format(self.user)

    @staticmethod
    def __calculate_cart_price_after_discount(total, discount_code):
        """Calculate cart price after discount
        :param total: float
        :param discount_code: DiscountCode
        :return: float
        """

        # if its zero return
        if not total:
            return total

        # multiple logics based on discount type
        if discount_code.kind == 'percent':
            total = total - (total * discount_code.percentage)
        else:
            total = total - discount_code.amount

        return total

    @property
    def total_price(self):
        """Total price of cart
        :return: float
        """
        total = self.items.aggregate(
            total=Sum(F('product__final_price') * F('quantity')))['total']

        # check if it has discount
        if self.discount_code:
            total = self.__calculate_cart_price_after_discount(total, self.discount_code)

        return total if total else 0.0

    def add_product(self, product, quantity):
        """Add product to cart
        :param product: Product
        :param quantity: int
        """
        if self.step not in ['initial', 'pending']:
            raise Exception('Cart is not in initial step')
        cart_item = self.items.filter(product=product).first()
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart=self,
                product=product,
                quantity=quantity
            )

    def update_product(self, product, quantity):
        """Update product in cart
        :param product: Product
        :param quantity: int
        """
        if self.step not in ['initial', 'pending']:
            raise Exception('Cart is not in initial step')
        cart_item = self.items.filter(product=product).first()
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()

    def delete_product(self, product):
        """Delete product from cart
        :param product: Product
        """
        if self.step not in ['initial', 'pending']:
            raise Exception('Cart is not in initial step')
        cart_item = self.items.filter(product=product).delete()

    def update_address(self, address):
        """Update address of cart
        :param address: Address
        """
        if self.step not in ['initial', 'pending']:
            raise Exception('Cart is not in initial step')
        self.address = address
        self.save()

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')


class CartItem(TimeStampModelMixin):
    """
    Cart item model
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.final_price * self.quantity

    def __str__(self):
        return f'{self.product.title} - {self.quantity}'

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
