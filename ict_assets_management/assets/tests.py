from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Role
from donorbuyer.models import DonorBuyer
from .models import Asset

class AssetAPITest(APITestCase):

    def setUp(self):
        # Roles
        self.admin_role = Role.objects.create(name="ADMIN")
        self.asset_role = Role.objects.create(name="ASSET_MANAGER")
        self.auditor_role = Role.objects.create(name="AUDITOR")

        # Users
        self.admin = User.objects.create_user(username="admin", password="admin123", role=self.admin_role)
        self.asset_manager = User.objects.create_user(username="asset", password="asset123", role=self.asset_role)
        self.auditor = User.objects.create_user(username="auditor", password="audit123", role=self.auditor_role)

        # DonorBuyer
        self.donor = DonorBuyer.objects.create(name="Donor 1", type="donor")

        # Sample Asset
        self.asset = Asset.objects.create(
            name="Laptop A",
            category="Electronics",
            serial_number="SN12345",
            model="Dell XPS",
            purchase_date="2023-01-01",
            value=1200.00,
            status="in_storage",
            condition="new",
            donor_buyer=self.donor
        )

        self.list_url = "/api/asset/"
        self.detail_url = f"/api/asset/{self.asset.id}/"

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # LIST
    def test_list_assets_authenticated(self):
        self.authenticate(self.auditor)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_assets_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # CREATE
    def test_admin_can_create_asset(self):
        self.authenticate(self.admin)
        data = {
            "name": "Laptop B",
            "category": "Electronics",
            "serial_number": "SN67890",
            "model": "MacBook Pro",
            "purchase_date": "2023-02-01",
            "value": 2000.00,
            "status": "in_storage",
            "condition": "new",
            "donor_buyer": self.donor.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_asset_manager_can_create_asset(self):
        self.authenticate(self.asset_manager)
        data = {
            "name": "Monitor A",
            "category": "Electronics",
            "serial_number": "SN55555",
            "model": "Samsung",
            "purchase_date": "2023-03-01",
            "value": 300.00,
            "status": "in_storage",
            "condition": "new",
            "donor_buyer": self.donor.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auditor_cannot_create_asset(self):
        self.authenticate(self.auditor)
        data = {
            "name": "Keyboard A",
            "category": "Electronics",
            "serial_number": "SN99999",
            "purchase_date": "2023-03-05",
            "value": 50.00,
            "status": "in_storage",
            "condition": "new",
            "donor_buyer": self.donor.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # RETRIEVE
    def test_authenticated_user_can_retrieve_asset(self):
        self.authenticate(self.auditor)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # UPDATE
    def test_admin_can_update_asset(self):
        self.authenticate(self.admin)
        data = {"name": "Laptop A Updated", "category": "Electronics", "serial_number": self.asset.serial_number,
                "purchase_date": "2023-01-01", "value": 1200.00, "status": "in_storage", "condition": "new",
                "donor_buyer": self.donor.id, "model": "Dell XPS"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_asset_manager_can_update_asset(self):
        self.authenticate(self.asset_manager)
        data = {"name": "Laptop A Updated By Asset Manager", "category": "Electronics", "serial_number": self.asset.serial_number,
                "purchase_date": "2023-01-01", "value": 1200.00, "status": "in_storage", "condition": "new",
                "donor_buyer": self.donor.id, "model": "Dell XPS"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auditor_cannot_update_asset(self):
        self.authenticate(self.auditor)
        data = {"name": "Invalid Update", "category": "Electronics"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE
    def test_admin_can_delete_asset(self):
        self.authenticate(self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_asset_manager_cannot_delete_asset(self):
        self.authenticate(self.asset_manager)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


#filter by status and category, search by name, serial number, model, 
# and valueorder by name and purchase date can be tested similarly by creating multiple assets with different values 
# and asserting the response of the list endpoint with appropriate query parameters.  

    def test_filter_assets_by_status(self):
        self.authenticate(self.admin)

        # Create assets with different statuses
        Asset.objects.create(
            name="Printer A", category="Electronics", serial_number="SN1000",
            model="HP", purchase_date="2023-01-10", value=200,
            status="in_use", condition="good", donor_buyer=self.donor
        )
        Asset.objects.create(
            name="Monitor B", category="Electronics", serial_number="SN2000",
            model="Samsung", purchase_date="2023-02-10", value=300,
            status="in_storage", condition="new", donor_buyer=self.donor
        )

        # Filter by in_storage
        response = self.client.get(f"{self.list_url}?status=in_storage")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for asset in response.data:
            self.assertEqual(asset["status"], "in_storage")


    def test_filter_assets_by_category(self):
        self.authenticate(self.admin)

        # Create assets with different categories
        Asset.objects.create(
            name="Table A", category="Furniture", serial_number="SN3000",
            model="Ikea", purchase_date="2023-03-01", value=150,
            status="in_storage", condition="new", donor_buyer=self.donor
        )
        Asset.objects.create(
            name="Laptop B", category="Electronics", serial_number="SN4000",
            model="Dell", purchase_date="2023-03-05", value=1200,
            status="in_use", condition="good", donor_buyer=self.donor
        )

        response = self.client.get(f"{self.list_url}?category=Electronics")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for asset in response.data:
            self.assertEqual(asset["category"], "Electronics")


#by name serial and model

    def test_search_assets_by_name(self):
        self.authenticate(self.admin)

        Asset.objects.create(
            name="Router X", category="Networking", serial_number="SN5000",
            model="Cisco", purchase_date="2023-04-01", value=500,
            status="in_use", condition="good", donor_buyer=self.donor
        )

        response = self.client.get(f"{self.list_url}?search=Router")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Router" in asset["name"] for asset in response.data))


    def test_search_assets_by_serial_number(self):
        self.authenticate(self.admin)

        Asset.objects.create(
            name="Switch Y", category="Networking", serial_number="SN6000",
            model="Cisco", purchase_date="2023-05-01", value=600,
            status="in_use", condition="good", donor_buyer=self.donor
        )

        response = self.client.get(f"{self.list_url}?search=SN6000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["serial_number"], "SN6000")


#ordering test

    def test_order_assets_by_name(self):
        self.authenticate(self.admin)

        Asset.objects.create(
            name="Z Asset", category="Electronics", serial_number="SN7000",
            model="Dell", purchase_date="2023-06-01", value=1200,
            status="in_storage", condition="new", donor_buyer=self.donor
        )
        Asset.objects.create(
            name="A Asset", category="Electronics", serial_number="SN8000",
            model="HP", purchase_date="2023-07-01", value=1300,
            status="in_storage", condition="new", donor_buyer=self.donor
        )

        response = self.client.get(f"{self.list_url}?ordering=name")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [asset["name"] for asset in response.data]
        self.assertEqual(names, sorted(names))

