from django.contrib import admin

from carts.models import Cart, CartItem, Address


class CartItemTabularInline(admin.TabularInline):
    """Cart item tabular inline"""
    model = CartItem
    fk_name = 'cart'
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created',)
    raw_id_fields = ['address']
    inlines = [CartItemTabularInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created',)
