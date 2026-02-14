from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Role  
from rest_framework.authtoken.models import Token


class AuthAPITestCase(APITestCase):
    def setUp(self):
        # Create roles
        self.admin_role = Role.objects.create(name="ADMIN", description="Admin user")
        
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            role=self.admin_role
        )

        # Endpoints
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_login_success(self):
        """Test successful login returns token and user info"""
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "testpassword123"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], "testuser")
        self.assertEqual(response.data['user']['role'], "ADMIN")

    def test_login_failure_wrong_credentials(self):
        """Test login fails with wrong password"""
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "wrongpassword"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data or response.data.keys())

    def test_logout_success(self):
        """Test logout invalidates token"""
        # First, log in and get token
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Successfully logged out.")

        # Token should be deleted
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_unauthenticated(self):
        """Test logout fails if not authenticated"""
        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
