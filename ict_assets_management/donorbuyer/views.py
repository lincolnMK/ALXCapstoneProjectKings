from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import DonorBuyer
from .serializers import DonorBuyerSerializer

from ict_assets_management.permissions import RoleBasedPermission

#viewsets

class DonorBuyerViewSet(viewsets.ModelViewSet):
    queryset = DonorBuyer.objects.all()
    serializer_class = DonorBuyerSerializer
    permission_classes = [RoleBasedPermission]
    role_permissions = {
    "list": ["ADMIN", "ASSET_MANAGER", "AUDITOR"],
    "retrieve": ["ADMIN", "ASSET_MANAGER", "AUDITOR"],
    "create": ["ADMIN", "ASSET_MANAGER"],
    "update": ["ADMIN"],
    "partial_update": ["ADMIN"],
    "destroy": ["ADMIN"],
}


    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'type', 'contact_person', 'email']
    ordering_fields = ['name', 'type', 'created_at']
    ordering = ['name']
