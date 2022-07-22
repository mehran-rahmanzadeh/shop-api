from django.db import models
from django.utils.translation import ugettext_lazy as _

from painless.utils.models.mixins import TimeStampModelMixin


class Product(TimeStampModelMixin):
    """
    Product model
    """
    title = models.CharField(
        _('Title'),
        max_length=255
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=255,
        unique=True
    )
    description = models.TextField(
        _('Description'),
        blank=True
    )
    base_price = models.DecimalField(
        _('Base price'),
        max_digits=6,
        decimal_places=2
    )
    discount_amount = models.DecimalField(
        _('Discount amount'),
        max_digits=6,
        decimal_places=2,
        default=0
    )
    final_price = models.DecimalField(
        _('Final price'),
        max_digits=6,
        decimal_places=2,
        default=0
    )
    has_discount = models.BooleanField(
        _('Has discount'),
        default=False
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
        verbose_name=_('Category')
    )
    quantity = models.PositiveIntegerField(
        _('Quantity'),
        default=0
    )
    image = models.ImageField(
        _('Image'),
        upload_to='products/',
        blank=True
    )

    def get_final_price(self):
        return self.base_price - self.discount_amount if self.has_discount else self.base_price

    @property
    def discount_percentage(self):
        return (self.discount_amount / self.base_price) * 100 if self.has_discount else 0

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.final_price = self.get_final_price()
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
