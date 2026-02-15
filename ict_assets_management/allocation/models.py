from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.conf import settings


# Create your models here.
class Allocation(models.Model):
    inventory_item = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, related_name='allocations')
    allocated_to = models.CharField(max_length=255)
    location = models.ForeignKey('location.Location', on_delete=models.CASCADE, related_name='allocations')
    allocation_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('allocated', 'Allocated'), ('returned', 'Returned')])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"Allocation of {self.inventory_item} to {self.allocated_to} on {self.allocation_date}"    
    class Meta:
        verbose_name = "Allocation"
        verbose_name_plural = "Allocations"
        ordering = ['-allocation_date']
        