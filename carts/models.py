from django.db import models
from django.conf import settings
from django.db.models import Sum, F
from django.utils.translation import ugettext_lazy as _

from painless.utils.models.mixins import TimeStampModelMixin


class Address(TimeStampModelMixin):
    """
    Address model
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User')
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
        max_length=255
    )
    country = models.CharField(
        _('Country'),
        max_length=255
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
        verbose_name=_('User')
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Address')
    )

    # TODO: should add discount_code field

    def __str__(self):
        return '{}'.format(self.user)

    @property
    def total_price(self):
        return self.items.aggregate(
            total=Sum(F('product__final_price') * F('quantity')))['total']

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
