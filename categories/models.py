from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from painless.utils.models.mixins import TimeStampModelMixin


class Category(TimeStampModelMixin, MPTTModel):
    """Category model class
    uses MPTTModel to create a tree structure
    """
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(
        _('Slug'),
        max_length=255,
        unique=True,
        allow_unicode=True
    )
    description = models.TextField(_('Description'))
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name=_('Parent')
    )
    order = models.IntegerField(
        _('Order'),
        blank=True,
        null=True,
        default=1
    )
    image = models.ImageField(
        _('Image'),
        upload_to='categories',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('order',)

    class MPTTMeta:
        order_insertion_by = ['order']

    def __str__(self):
        return self.title
