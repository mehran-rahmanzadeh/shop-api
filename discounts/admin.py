from django.contrib import admin

from discounts.models import DiscountCode


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    """
    Discount code admin
    """
    list_display = ('code', 'kind', 'percentage', 'amount', 'is_active')
    list_filter = ('kind', 'is_active')
    search_fields = ('code', 'used_by__username')
    save_on_top = True
    save_as = True
    actions = ('activate', 'deactivate')

    def activate(self, request, queryset):
        """Activate selected discount codes"""
        queryset.update(is_active=True)

    def deactivate(self, request, queryset):
        """Deactivate selected discount codes"""
        queryset.update(is_active=False)

    activate.short_description = 'Activate selected discount codes'
    deactivate.short_description = 'Deactivate selected discount codes'

    def get_queryset(self, request):
        """Get queryset"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('used_by')
