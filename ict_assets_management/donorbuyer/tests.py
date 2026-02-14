from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import DonorBuyer
from users.models import User, Role

from rest_framework.authtoken.models import Token


class DonorBuyerAPITestCase(APITestCase):
    def setUp(self):
        # Create roles
        self.admin_role = Role.objects.create(name="ADMIN")
        self.asset_manager_role = Role.objects.create(name="ASSET_MANAGER")
        self.auditor_role = Role.objects.create(name="AUDITOR")

        # Create users for each role
        self.admin = User.objects.create_user(username="admin", password="admin123", role=self.admin_role)
        self.asset_manager = User.objects.create_user(username="assetmgr", password="asset123", role=self.asset_manager_role)
        self.auditor = User.objects.create_user(username="auditor", password="audit123", role=self.auditor_role)

        # Create a DonorBuyer instance
        self.donorbuyer = DonorBuyer.objects.create(
            name="Test Donor",
            type="donor",
            contact_person="John Doe",
            email="donor@example.com",
            phone_number="123456789"
        )

        self.url_list = reverse('donorbuyer-list')  # from DefaultRouter
        self.url_detail = reverse('donorbuyer-detail', args=[self.donorbuyer.id])

    def authenticate(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # ---- List Tests ----
    def test_list_donorbuyer_admin(self):
        self.authenticate(self.admin)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_donorbuyer_asset_manager(self):
        self.authenticate(self.asset_manager)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_donorbuyer_auditor(self):
        self.authenticate(self.auditor)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ---- Create Tests ----
    def test_create_donorbuyer_admin(self):
        self.authenticate(self.admin)
        data = {"name": "New Donor", "type": "donor", "contact_person": "Alice"}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "New Donor")

    def test_create_donorbuyer_asset_manager(self):
        self.authenticate(self.asset_manager)
        data = {"name": "New Buyer", "type": "buyer", "contact_person": "Bob", "email": "buyer@example.com" }
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_donorbuyer_auditor_forbidden(self):
        self.authenticate(self.auditor)
        data = {"name": "Test", "type": "donor"}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---- Retrieve Tests ----
    def test_retrieve_donorbuyer_admin(self):
        self.authenticate(self.admin)
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_donorbuyer_non_admin_forbidden(self):
        self.authenticate(self.asset_manager)
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---- Update Tests ----
    def test_update_donorbuyer_admin(self):
        self.authenticate(self.admin)
        data = {"name": "Updated Donor", "type": "donor"}
        response = self.client.put(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Donor")

    def test_update_donorbuyer_non_admin_forbidden(self):
        self.authenticate(self.asset_manager)
        data = {"name": "Should Fail"}
        response = self.client.put(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---- Delete Tests ----
    def test_delete_donorbuyer_admin(self):
        self.authenticate(self.admin)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_donorbuyer_non_admin_forbidden(self):
        self.authenticate(self.asset_manager)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
