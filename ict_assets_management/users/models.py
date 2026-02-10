from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True
    )
    
    history = HistoricalRecords() 
    
    def is_admin(self):
        return self.role and self.role.name == "ADMIN"

    def is_asset_manager(self):
        return self.role and self.role.name == "ASSET_MANAGER"

    def is_auditor(self):
        return self.role and self.role.name == "AUDITOR"