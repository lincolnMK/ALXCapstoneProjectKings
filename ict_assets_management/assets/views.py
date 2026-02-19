from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Asset
from .serializers import AssetSerializer
from ict_assets_management.permissions import RoleBasedPermission



class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [RoleBasedPermission]
    role_permissions = {
    "list": ["ADMIN", "ASSET_MANAGER", "AUDITOR"],
    "retrieve": ["ADMIN", "ASSET_MANAGER", "AUDITOR"],
    "create": ["ADMIN", "ASSET_MANAGER"],
    "update": ["ADMIN", "ASSET_MANAGER"],
    "partial_update": ["ADMIN"],
    "destroy": ["ADMIN"],
}

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['name', 'serial_number', 'model']
    ordering_fields = ['name', 'purchase_date']
