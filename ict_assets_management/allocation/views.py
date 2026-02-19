from django.shortcuts import render
from rest_framework.permissions import BasePermission
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from ict_assets_management.permissions import RoleBasedPermission
from .models import Allocation
from .serializers import AllocationSerializer



# Create your views here.
#permissions for the model:


class AllocationViewSet(viewsets.ModelViewSet):
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer
    permission_classes = [RoleBasedPermission]
    role_permissions = {
    "list": ["ADMIN", "ASSET_MANAGER", "AUDITOR"],
    "retrieve": ["ADMIN", "ASSET_MANAGER", "AUDITOR"],
    "create": ["ADMIN", "ASSET_MANAGER"],
    "update": ["ADMIN", "ASSET_MANAGER"],
    "partial_update": ["ADMIN", "ASSET_MANAGER"],
    "destroy": ["ADMIN"],
}

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'allocated_to', 'inventory_item',   'location',   'allocation_date', 'return_date']
    search_fields = ['allocated_to', 
                     'notes', 
                     'inventory_item__name',
                     'location__name', 
                     'inventory_item__serial_number']
    ordering_fields = ['allocation_date', 'return_date', 'created_at', 'status']

    def perform_create(self, serializer):
        # Automatically set created_by to the logged-in user
        serializer.save(created_by=self.request.user)
