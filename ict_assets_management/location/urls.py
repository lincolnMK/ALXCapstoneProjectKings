from rest_framework.routers import DefaultRouter
from .views import LocationViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('', LocationViewSet, basename='location')  # empty string because prefix is in project urls

urlpatterns = [
    path('', include(router.urls)),
]
