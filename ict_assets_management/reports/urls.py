from django.urls import path
from .views import ReportsView

urlpatterns = [
    path("", ReportsView.as_view(), name="reports"),
]



'''
type parameter useed to call for reports api:
/api/reports/?type=asset-summary
/api/reports/?type=allocation-by-location
/api/reports/?type=allocation-by-user
/api/reports/?type=allocation-date-range&start=2024-01-01&end=2024-12-31

'''