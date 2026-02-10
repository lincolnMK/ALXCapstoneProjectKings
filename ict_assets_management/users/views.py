from django.shortcuts import render
from rest_framework.permissions import BasePermission
from rest_framework import generics
from .models import User
from .serializers import UserSerializer


#permission class to restrict access
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role and
            request.user.role.name == "ADMIN"
        )
        
class IsAdminOrAuditor(BasePermission):
    """
    Allows access to ADMIN and AUDITOR roles.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role
            and request.user.role.name in ["ADMIN", "AUDITOR"]
        )        
        
        
        

# Create your views here.

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]  # Only Admins can list & create

# Retrieve / Update / Delete a single user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]  # O