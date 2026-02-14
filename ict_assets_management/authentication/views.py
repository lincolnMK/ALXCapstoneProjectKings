from time import timezone
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from .serializers import LoginSerializer
from django.utils import timezone

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Update last_login to track login
        user.last_login = timezone.now()
        user.save()  # This triggers simple_history to record the change
       
        # Generate or get token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role.name if user.role else None,
            }
        })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user.last_logout = timezone.now()
        user.save()  # simple_history will track this change
        request.user.auth_token.delete()  # Delete token
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
