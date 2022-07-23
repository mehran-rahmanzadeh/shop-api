from django.urls import path
from rest_framework.routers import DefaultRouter

from search.api.v1.views import ProductElasticsearchViewSet, ProductPostgresTrigramSearchViewset

router = DefaultRouter()
router.register(r'search/trigram', ProductPostgresTrigramSearchViewset, basename='trigram-search')

urlpatterns = [
    path('search/elastic/', ProductElasticsearchViewSet.as_view(), name='search-elastic'),
] + router.urls
