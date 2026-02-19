from django.shortcuts import render
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ict_assets_management.permissions import RoleBasedPermission
from .models import Location
from .serializers import LocationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


# Create your views here.

from rest_framework.permissions import BasePermission, SAFE_METHODS

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    role_permissions = {
    "list": ["ADMIN", "ASSET_MANAGER", "AUDITOR"],
    "retrieve": ["ADMIN", "ASSET_MANAGER", "AUDITOR"],
    "create": ["ADMIN", "ASSET_MANAGER"],
    "update": ["ADMIN"],
    "partial_update": ["ADMIN"],
    "destroy": ["ADMIN"],
}

    # Optional but recommended
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type", "building", "floor"]
    search_fields = ["name", "address", "room"]
    ordering_fields = ["name", "created_at"]
