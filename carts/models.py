from django.db import models
from django.conf import settings
from django.db.models import Sum, F
from django.utils.translation import ugettext_lazy as _

from painless.utils.models.mixins import TimeStampModelMixin


class Cart(TimeStampModelMixin):
    """
    Cart model
    """
    STEP_CHOICES = (
        ('initial', _('Initial')),
        ('pending', _('Pending')),
        ('paid', _('Paid'))
    )
    step = models.CharField(_('Step'), choices=STEP_CHOICES, max_length=20, default='initial')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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
