from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Role, User

class AuthAPITestCase(APITestCase):

    def setUp(self):
        # Create role
        self.admin_role = Role.objects.create(name="ADMIN", description="Admin user")

        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            role=self.admin_role
        )

        # Endpoint URLs
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.refresh_url = reverse('token_refresh')  # SimpleJWT refresh endpoint

    # LOGIN SUCCESS
    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "testpassword123"},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], "testuser")
        self.assertEqual(response.data['user']['role'], "ADMIN")

    # LOGIN FAILURE
    def test_login_failure_wrong_credentials(self):
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "wrongpassword"},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # LOGOUT SUCCESS
    def test_logout_success(self):
        # Generate JWT tokens
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Authenticate request with access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Logout using refresh token (blacklist)
        response = self.client.post(
            self.logout_url,
            {"refresh": str(refresh)},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Successfully logged out.")

    # LOGOUT UNAUTHENTICATED
    def test_logout_unauthenticated(self):
        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # TOKEN REFRESH
    def test_token_refresh(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(
            self.refresh_url,
            {"refresh": str(refresh)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
