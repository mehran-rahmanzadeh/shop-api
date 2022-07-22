from rest_framework.routers import DefaultRouter

from products.api.v1.views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = router.urls
