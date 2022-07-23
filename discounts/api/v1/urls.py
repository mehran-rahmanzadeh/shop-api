from django.urls import path

from discounts.api.v1.views import ApplyDiscountCodeAPIView

urlpatterns = [
    path('apply-discount-code/', ApplyDiscountCodeAPIView.as_view(), name='apply-discount-code')
]
