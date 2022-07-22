from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    """Category admin class"""
    list_display = ('title', 'slug', 'parent', 'order', 'created', 'modified')
    list_display_links = ('title', 'slug')
    list_editable = ('order',)
    list_filter = ('created', 'modified')
    search_fields = ('title', 'slug')
    mptt_level_indent = 25
    prepopulated_fields = {'slug': ('title',)}
