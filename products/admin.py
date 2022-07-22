from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'final_price', 'base_price', 'discount_amount', 'has_discount', 'quantity')
    list_filter = ('category', 'has_discount')
    search_fields = ('title', 'description')
    ordering = ('-created',)
    readonly_fields = ('created', 'modified')
    fieldsets = (
        (None, {
            'fields': (
                'title', 'category', 'final_price',
                'base_price', 'discount_amount',
                'has_discount', 'quantity')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Meta', {
            'fields': ('slug', 'description')
        }),
        ('Timestamps', {
            'fields': ('created', 'modified')
        }),
    )
    prepopulated_fields = {'slug': ('title',)}