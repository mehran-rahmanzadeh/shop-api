from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from painless.utils.models.mixins import TimeStampModelMixin


class DiscountCode(TimeStampModelMixin):
    """
    Discount code model
    kind: (percentage, fixed amount)
    code: unique code
    percentage: percentage of discount
    amount: fixed amount of discount
    used_by: list of users who used this code
    is_active: is this code active
    """
    KIND_CHOICES = (
        ('percent', _('Percentage')),
        ('amount', _('Amount')),
    )
    kind = models.CharField(_('Kind'), max_length=10, choices=KIND_CHOICES)
    code = models.CharField(_('Code'), max_length=255, unique=True)
    percentage = models.PositiveSmallIntegerField(_('Percentage'), null=True, blank=True)
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2, null=True, blank=True)
    used_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('Used by'),
        blank=True, editable=False
    )
    is_active = models.BooleanField(_('Is active'), default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Discount code')
        verbose_name_plural = _('Discount codes')
        ordering = ('-created',)
