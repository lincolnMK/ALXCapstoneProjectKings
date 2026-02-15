from django.shortcuts import render
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Location
from .serializers import LocationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


# Create your views here.


#permissions for the model:



from rest_framework.permissions import BasePermission, SAFE_METHODS


class LocationPermission(BasePermission):
    """
    Permissions:
    - List & Retrieve → Any authenticated user
    - Create → Admin OR Asset Manager
    - Update → Admin only
    - Delete → Admin only
    """

    def has_permission(self, request, view):

        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # GET, HEAD, OPTIONS → All authenticated users
        if request.method in SAFE_METHODS:
            return True

        # POST → Admin or Asset Manager
        if request.method == "POST":
            return request.user.is_admin() or request.user.is_asset_manager()

        # PUT, PATCH, DELETE → Admin only
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user.is_admin()

        return False

 

 #viewsets
 



class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, LocationPermission]

    # Optional but recommended
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type", "building", "floor"]
    search_fields = ["name", "address", "room"]
    ordering_fields = ["name", "created_at"]
