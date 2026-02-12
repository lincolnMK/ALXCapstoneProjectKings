from django.contrib import admin

from .models import Asset

# Register your models here.

class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'status', 'purchase_date', 'warranty_expiry_date') 

admin.site.register(Asset, AssetAdmin)
