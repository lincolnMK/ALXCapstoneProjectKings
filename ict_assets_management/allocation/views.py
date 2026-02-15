from django.shortcuts import render
from rest_framework.permissions import BasePermission
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Allocation
from .serializers import AllocationSerializer



# Create your views here.
#permissions for the model:



class AllocationPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # List & Retrieve → all authenticated users
        if view.action in ['list', 'retrieve']:
            return True

        # Create → Admin or Asset Manager
        if view.action == 'create':
            return user.is_admin() or user.is_asset_manager()

        # Update → Admin or Asset Manager
        if view.action in ['update', 'partial_update']:
            return user.is_admin() or user.is_asset_manager()

        # Delete → Admin only
        if view.action == 'destroy':
            return user.is_admin()

        return False

#viewsets

class AllocationViewSet(viewsets.ModelViewSet):
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer
    permission_classes = [AllocationPermission]

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
