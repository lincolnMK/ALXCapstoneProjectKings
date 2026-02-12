from django.db import models

# Create your models here.
from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class DonorBuyer(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, choices=[('donor', 'Donor'), ('buyer', 'Buyer')])
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Donor/Buyer"
        verbose_name_plural = "Donors/Buyers"
        ordering = ['name']