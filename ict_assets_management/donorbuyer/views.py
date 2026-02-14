from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import DonorBuyer
from .serializers import DonorBuyerSerializer



# Create your views here.
#permissions 

from rest_framework import permissions

class DonorBuyerPermission(permissions.BasePermission):
    """
    Role-based permissions:
    - Admin: full access
    - Asset Manager: can create and list
    - Auditor: can only list
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if view.action in ['list']:
            # List accessible by Admin, Asset Manager, Auditor
            return user.is_admin() or user.is_asset_manager() or user.is_auditor()

        if view.action in ['create']:
            # Create accessible by Admin, Asset Manager
            return user.is_admin() or user.is_asset_manager()

        # For retrieve/update/delete
        return user.is_admin()

    def has_object_permission(self, request, view, obj):
        # Object-level permissions same as above
        return self.has_permission(request, view)


#viewsets

class DonorBuyerViewSet(viewsets.ModelViewSet):
    queryset = DonorBuyer.objects.all()
    serializer_class = DonorBuyerSerializer
    permission_classes = [DonorBuyerPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'type', 'contact_person', 'email']
    ordering_fields = ['name', 'type', 'created_at']
    ordering = ['name']
