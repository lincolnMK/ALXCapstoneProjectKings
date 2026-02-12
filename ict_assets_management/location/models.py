from django.db import models
from simple_history.models import HistoricalRecords

class Location(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[('office', 'Office'), ('storage', 'Storage'), ('data_center', 'Data Center'), ('other', 'Other')])
    address = models.TextField(blank=True)
    building = models.CharField(max_length=255, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    room = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['name']
# Create your models here.
