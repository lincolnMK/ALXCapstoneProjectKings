from django.db import models
from simple_history.models import HistoricalRecords
from donorbuyer.models import DonorBuyer

# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    model= models.TextField(blank=True)
    purchase_date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('in_use', 'In Use'), ('in_storage', 'In Storage'), ('under_maintenance', 'Under Maintenance'), ('retired', 'Retired')])
    condition = models.CharField(max_length=50, choices=[('new', 'New'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')])
    warranty_expiry_date = models.DateField(null=True, blank=True)
    donor_buyer = models.ForeignKey('donorbuyer.DonorBuyer',on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
        ordering = ['name']