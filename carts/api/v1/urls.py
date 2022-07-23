from rest_framework.routers import DefaultRouter

from carts.api.v1.views import CartViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')

urlpatterns = router.urls
