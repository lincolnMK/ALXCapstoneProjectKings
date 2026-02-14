from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonorBuyerViewSet

router = DefaultRouter()
router.register('', DonorBuyerViewSet, basename='donorbuyer')  # empty string because prefix is in project urls

urlpatterns = [
    path('', include(router.urls)),
]
