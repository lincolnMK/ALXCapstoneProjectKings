

# Create your tests here.
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User, Role
from rest_framework import status

class UsersAPITest(APITestCase):

    def setUp(self):
        # Create roles
        self.admin_role = Role.objects.create(name="ADMIN")
        self.asset_manager_role = Role.objects.create(name="ASSET_MANAGER")
        self.auditor_role = Role.objects.create(name="AUDITOR")

        # Create admin user
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="AdminPass123",
            role=self.admin_role
        )

        # Create non-admin user
        self.auditor_user = User.objects.create_user(
            username="auditor",
            email="auditor@example.com",
            password="AuditorPass123",
            role=self.auditor_role
        )

        # API client
        self.client = APIClient()

    def test_list_users_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)

    def test_list_users_non_admin(self):
        self.client.force_authenticate(user=self.auditor_user)
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('user-list-create')
        data = {
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": self.asset_manager_role.id,
            "password": "SecurePass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username="john_doe").exists(), True)

    def test_update_user_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        user_to_update = self.auditor_user
        url = reverse('user-detail', kwargs={'pk': user_to_update.id})
        data = {"first_name": "AuditorUpdated", "role": self.admin_role.id}
        response = self.client.patch(url, data, format='json')  # PATCH instead of PUT

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_to_update.refresh_from_db()
        self.assertEqual(user_to_update.first_name, "AuditorUpdated")
        self.assertEqual(user_to_update.role.id, self.admin_role.id)

    def test_delete_user_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        user_to_delete = self.auditor_user
        url = reverse('user-detail', kwargs={'pk': user_to_delete.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user_to_delete.id).exists())
