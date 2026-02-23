from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from assets.models import Asset
from allocation.models import Allocation
from location.models import Location
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework.permissions import BasePermission
User = get_user_model()
from ict_assets_management.permissions import RoleBasedPermission


class ReportsView(viewsets.ViewSet):
    permission_classes = [RoleBasedPermission]
    role_permissions = {
        "list": ["ADMIN", "AUDITOR"],       # GET /api/reports/
        "retrieve": ["ADMIN", "AUDITOR"],   # GET /api/reports/{pk}/ if needed
    }

    def list(self, request):
        """
        Handles GET /api/reports/?type=<report_type>
        """
        report_type = request.query_params.get("type")

        if report_type == "asset-summary":
            return self.asset_summary()

        elif report_type == "allocation-by-location":
            return self.allocation_by_location()

        elif report_type == "allocation-by-user":
            return self.allocation_by_user()

        elif report_type == "allocation-date-range":
            return self.allocation_date_range(request)

        return Response({"error": "Invalid report type"}, status=400)

    # --------------------------
    # REPORT METHODS
    # --------------------------

    def asset_summary(self):
        total = Asset.objects.count()
        by_status = Asset.objects.values("status").annotate(count=Count("id"))

        return Response({
            "total_assets": total,
            "by_status": by_status
        })

    def allocation_by_location(self):
        data = Location.objects.annotate(
            total_allocations=Count("allocations")
        ).values("id", "name", "total_allocations")

        return Response(data)

    def allocation_by_user(self):
        data = User.objects.annotate(
            total_allocations=Count("allocations")
        ).values("id", "username", "total_allocations")

        return Response(data)

    def allocation_date_range(self, request):
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if not start or not end:
            return Response(
                {"error": "Start and end dates required"},
                status=400
            )

        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()

        allocations = Allocation.objects.filter(
            allocation_date__range=(start_date, end_date)
        ).count()

        return Response({
            "start_date": start,
            "end_date": end,
            "total_allocations": allocations
        })
