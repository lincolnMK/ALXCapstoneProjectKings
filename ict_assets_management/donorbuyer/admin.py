from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DonorBuyer

# Register your models here.
class DonorBuyerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'address', 'type') 

admin.site.register(DonorBuyer, DonorBuyerAdmin)