from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Asset
from .serializers import AssetSerializer

from rest_framework.permissions import BasePermission


#permissions for the model:

class AssetPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # List & Retrieve allowed for all authenticated users
        if view.action in ['list', 'retrieve']:
            return True

        # Create allowed for Admin & Asset Manager
        if view.action == 'create':
            return user.is_admin() or user.is_asset_manager()

        # Update allowed for Admin & Asset Manager
        if view.action in ['update', 'partial_update']:
            return user.is_admin() or user.is_asset_manager()

        # Delete only Admin
        if view.action == 'destroy':
            return user.is_admin()

        return False

#viewsets


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [AssetPermission]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['name', 'serial_number', 'model']
    ordering_fields = ['name', 'purchase_date']
