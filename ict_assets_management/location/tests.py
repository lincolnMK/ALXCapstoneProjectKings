from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from users.models import User, Role
from .models import Location


class LocationAPITest(APITestCase):

    def setUp(self):

        # Create roles
        self.admin_role = Role.objects.create(name="ADMIN")
        self.asset_role = Role.objects.create(name="ASSET_MANAGER")
        self.auditor_role = Role.objects.create(name="AUDITOR")

        # Create users
        self.admin = User.objects.create_user(
            username="admin",
            password="admin123",
            role=self.admin_role
        )

        self.asset_manager = User.objects.create_user(
            username="asset",
            password="asset123",
            role=self.asset_role
        )

        self.auditor = User.objects.create_user(
            username="auditor",
            password="audit123",
            role=self.auditor_role
        )

        # Create sample location
        self.location = Location.objects.create(
            name="Main Office",
            type="office",
            address="City Center"
        )

        self.list_url = "/api/location/"
        self.detail_url = f"/api/location/{self.location.id}/"

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # ---------------------------------------
    # LIST TESTS
    # ---------------------------------------

    def test_list_locations_authenticated(self):
        self.authenticate(self.auditor)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_locations_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ---------------------------------------
    # CREATE TESTS
    # ---------------------------------------

    def test_admin_can_create_location(self):
        self.authenticate(self.admin)

        data = {
            "name": "Storage A",
            "type": "storage",
            "address": "Warehouse Area"
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_asset_manager_can_create_location(self):
        self.authenticate(self.asset_manager)

        data = {
            "name": "Data Center 1",
            "type": "data_center",
            "address": "Tech Park"
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auditor_cannot_create_location(self):
        self.authenticate(self.auditor)

        data = {
            "name": "Unauthorized Location",
            "type": "office"
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------------------------------------
    # RETRIEVE TESTS
    # ---------------------------------------

    def test_authenticated_user_can_retrieve_location(self):
        self.authenticate(self.auditor)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ---------------------------------------
    # UPDATE TESTS
    # ---------------------------------------

    def test_admin_can_update_location(self):
        self.authenticate(self.admin)

        data = {
            "name": "Updated Office",
            "type": "office",
            "address": "Updated Address"
        }

        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_asset_manager_cannot_update_location(self):
        self.authenticate(self.asset_manager)

        data = {
            "name": "Should Fail",
            "type": "office"
        }

        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------------------------------------
    # DELETE TESTS
    # ---------------------------------------

    def test_admin_can_delete_location(self):
        self.authenticate(self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_asset_manager_cannot_delete_location(self):
        self.authenticate(self.asset_manager)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#filtering test

    def test_filter_locations_by_type(self):
        self.authenticate(self.admin)

        # Create additional locations
        Location.objects.create(name="Storage A", type="storage")
        Location.objects.create(name="Office B", type="office")

        response = self.client.get(f"{self.list_url}?type=storage")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["type"], "storage")


    #search test
    def test_search_locations_by_name(self):
        self.authenticate(self.admin)

        Location.objects.create(name="Data Center Alpha", type="data_center")
        Location.objects.create(name="Branch Office", type="office")

        response = self.client.get(f"{self.list_url}?search=Alpha")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("Alpha", response.data[0]["name"])


    #ordering test
    def test_order_locations_by_name(self):
        self.authenticate(self.admin)

        Location.objects.create(name="Z Location", type="office")
        Location.objects.create(name="A Location", type="office")

        response = self.client.get(f"{self.list_url}?ordering=name")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        names = [loc["name"] for loc in response.data]
        self.assertEqual(names, sorted(names))
