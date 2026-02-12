from django.contrib import admin

# Register your models here.
from .models import Allocation

@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ('id',  'allocated_to', 'allocation_date', 'return_date', 'status')
