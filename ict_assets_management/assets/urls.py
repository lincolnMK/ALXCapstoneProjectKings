from rest_framework.routers import DefaultRouter
from .views import AssetViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('', AssetViewSet, basename='asset')  # empty string because prefix is in project urls

urlpatterns = [
    path('', include(router.urls)),
]
