from rest_framework.routers import DefaultRouter

from carts.api.v1.views import CartViewSet, AddressViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = router.urls
