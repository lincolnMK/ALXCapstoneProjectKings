from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Role
from assets.models import Asset
from location.models import Location
from donorbuyer.models import DonorBuyer
from .models import Allocation


class AllocationAPITest(APITestCase):

    def setUp(self):
        # Roles
        self.admin_role = Role.objects.create(name="ADMIN")
        self.asset_role = Role.objects.create(name="ASSET_MANAGER")
        self.auditor_role = Role.objects.create(name="AUDITOR")

        # Users
        self.admin = User.objects.create_user(
            username="admin", password="admin123", role=self.admin_role
        )
        self.asset_manager = User.objects.create_user(
            username="asset", password="asset123", role=self.asset_role
        )
        self.auditor = User.objects.create_user(
            username="auditor", password="audit123", role=self.auditor_role
        )

        # DonorBuyer
        self.donor = DonorBuyer.objects.create(name="Donor 1", type="donor")

        # Asset
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

        # Location
        self.location = Location.objects.create(
            name="Main Office",
            type="office",
            address="123 Main St",
        )

        self.list_url = "/api/allocation/"
        self.detail_url_template = "/api/allocation/{}/"

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # ------------------------
    # LIST
    # ------------------------

    def test_list_allocations_authenticated(self):
        self.authenticate(self.auditor)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_allocations_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ------------------------
    # CREATE
    # ------------------------

    def test_admin_can_create_allocation(self):
        self.authenticate(self.admin)
        data = {
            "inventory_id": self.asset.id,
            "location_id": self.location.id,
            "allocated_to": "John Doe",
            "status": "allocated"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["allocated_to"], "John Doe")

    def test_asset_manager_can_create_allocation(self):
        self.authenticate(self.asset_manager)
        data = {
            "inventory_id": self.asset.id,
            "location_id": self.location.id,
            "allocated_to": "Jane Smith",
            "status": "allocated"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auditor_cannot_create_allocation(self):
        self.authenticate(self.auditor)
        data = {
            "inventory_id": self.asset.id,
            "location_id": self.location.id,
            "allocated_to": "Auditor User",
            "status": "allocated"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------------
    # RETRIEVE
    # ------------------------

    def test_authenticated_user_can_retrieve_allocation(self):
        allocation = Allocation.objects.create(
            inventory_item=self.asset,
            allocated_to="John Doe",
            location=self.location,
            status="allocated",
            created_by=self.admin
        )

        self.authenticate(self.asset_manager)

        url = self.detail_url_template.format(allocation.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["allocated_to"], "John Doe")


# filter tests 
    def setUp_allocations_for_filtering(self):
        """Helper method to create multiple allocations for filtering tests."""
        self.allocation1 = Allocation.objects.create(
            inventory_item=self.asset,
            allocated_to="John Doe",
            location=self.location,
            status="allocated",
            created_by=self.admin
        )

        self.location2 = Location.objects.create(
            name="Branch Office",
            type="office",
            address="456 Branch St",
        )

        self.asset2 = Asset.objects.create(
            name="Monitor B",
            category="Electronics",
            serial_number="SN99999",
            model="HP 24",
            purchase_date="2023-02-01",
            value=400.00,
            status="in_storage",
            condition="new",
            donor_buyer=self.donor
        )

        self.allocation2 = Allocation.objects.create(
            inventory_item=self.asset2,
            allocated_to="Jane Smith",
            location=self.location2,
            status="returned",
            created_by=self.admin
        )


#filter by ststaus

    def test_filter_by_status(self):
        self.setUp_allocations_for_filtering()
        self.authenticate(self.admin)

        response = self.client.get(self.list_url, {"status": "returned"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "returned")

#filter by location
    def test_filter_by_location(self):
        self.setUp_allocations_for_filtering()
        self.authenticate(self.admin)

        response = self.client.get(self.list_url, {"location": self.location.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["location"]["id"], self.location.id)
        self.assertEqual(response.data[0]["status"], "allocated")

#filter by allocation date 

    def test_filter_by_allocation_date(self):
        self.setUp_allocations_for_filtering()
        self.authenticate(self.admin)

        allocation_date = self.allocation1.allocation_date

        response = self.client.get(self.list_url, {
            "allocation_date": allocation_date
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

#Search by allocated to

    def test_search_by_allocated_to(self):
        self.setUp_allocations_for_filtering()
        self.authenticate(self.admin)

        response = self.client.get(self.list_url, {"search": "John"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["allocated_to"], "John Doe")

#search by asset name

    def test_search_by_asset_name(self):
        self.setUp_allocations_for_filtering()
        self.authenticate(self.admin)

        response = self.client.get(self.list_url, {"search": "Monitor"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["inventory_item"]["name"], "Monitor B")


#search by location name
    def test_search_by_location_name(self):
        self.setUp_allocations_for_filtering()
        self.authenticate(self.admin)

        response = self.client.get(self.list_url, {"search": "Branch"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["location"]["name"], "Branch Office")

#order by status

    def test_order_by_status(self):
        self.setUp_allocations_for_filtering()
        self.authenticate(self.admin)

        response = self.client.get(self.list_url, {"ordering": "status"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["status"], "allocated")
        self.assertEqual(response.data[1]["status"], "returned")


#order by descending date

    def test_order_by_allocation_date_desc(self):
        self.setUp_allocations_for_filtering()
        self.authenticate(self.admin)

        response = self.client.get(self.list_url, {"ordering": "-allocation_date"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
