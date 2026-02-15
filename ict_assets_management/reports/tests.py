from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User, Role
from assets.models import Asset
from location.models import Location
from donorbuyer.models import DonorBuyer
from allocation.models import Allocation
from datetime import date, timedelta

class ReportsAPITest(APITestCase):

    def setUp(self):
        # Roles
        self.admin_role = Role.objects.create(name="ADMIN")
        self.auditor_role = Role.objects.create(name="AUDITOR")

        # Users
        self.admin = User.objects.create_user(username="admin", password="admin123", role=self.admin_role)
        self.auditor = User.objects.create_user(username="auditor", password="audit123", role=self.auditor_role)

        # DonorBuyer
        self.donor = DonorBuyer.objects.create(name="Donor 1", type="donor")

        # Assets
        self.asset1 = Asset.objects.create(
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

        self.asset2 = Asset.objects.create(
            name="Projector B",
            category="Electronics",
            serial_number="SN67890",
            model="Epson X200",
            purchase_date="2023-02-01",
            value=800.00,
            status="allocated",
            condition="good",
            donor_buyer=self.donor
        )

        # Locations
        self.location1 = Location.objects.create(name="Main Office", type="office", address="123 Main St")
        self.location2 = Location.objects.create(name="Branch Office", type="office", address="456 Branch St")

        # Allocations
        self.alloc1 = Allocation.objects.create(
            inventory_item=self.asset2,
            allocated_to="John Doe",
            location=self.location1,
            created_by=self.admin,
            status="allocated"
        )

        self.alloc2 = Allocation.objects.create(
            inventory_item=self.asset1,
            allocated_to="Jane Smith",
            location=self.location2,
            created_by=self.admin,
            status="returned",
            allocation_date=date.today() - timedelta(days=10)
        )

        self.url = reverse("reports")

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # -----------------------------
    # TEST REPORTS
    # -----------------------------

    def test_asset_summary_report(self):
        self.authenticate(self.admin)
        response = self.client.get(self.url, {"type": "asset-summary"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_assets", response.data)
        self.assertIn("by_status", response.data)
        self.assertEqual(response.data["total_assets"], 2)

    def test_allocation_by_location_report(self):
        self.authenticate(self.admin)
        response = self.client.get(self.url, {"type": "allocation-by-location"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 locations
        self.assertTrue(any(loc["total_allocations"] > 0 for loc in response.data))

    def test_allocation_by_user_report(self):
        self.authenticate(self.admin)
        response = self.client.get(self.url, {"type": "allocation-by-user"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(user["total_allocations"] > 0 for user in response.data))

    def test_allocation_date_range_report(self):
        self.authenticate(self.admin)
        start = (date.today() - timedelta(days=20)).strftime("%Y-%m-%d")
        end = date.today().strftime("%Y-%m-%d")
        response = self.client.get(self.url, {"type": "allocation-date-range", "start": start, "end": end})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_allocations", response.data)
        self.assertGreaterEqual(response.data["total_allocations"], 1)

    def test_invalid_report_type(self):
        self.authenticate(self.admin)
        response = self.client.get(self.url, {"type": "non-existent"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_unauthenticated_access(self):
        response = self.client.get(self.url, {"type": "asset-summary"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
