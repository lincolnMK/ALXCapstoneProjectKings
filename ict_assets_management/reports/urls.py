from django.urls import path
from .views import ReportsView

reports_list = ReportsView.as_view({'get': 'list'})
urlpatterns = [
    path('', reports_list, name='reports-list'),
    
]



'''
type parameter useed to call for reports api:
/api/reports/?type=asset-summary
/api/reports/?type=allocation-by-location
/api/reports/?type=allocation-by-user
/api/reports/?type=allocation-date-range&start=2024-01-01&end=2024-12-31

'''