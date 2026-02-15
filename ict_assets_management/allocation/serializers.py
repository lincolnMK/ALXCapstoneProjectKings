from rest_framework import serializers
from .models import Allocation
from assets.models import Asset
from location.models import Location
from assets.serializers import AssetSerializer
from location.serializers import LocationSerializer


class AllocationSerializer(serializers.ModelSerializer):
    # Nested read-only representations
    inventory_item = AssetSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    # Write-only IDs for creation
    inventory_id = serializers.PrimaryKeyRelatedField(
        queryset=Asset.objects.all(),
        source='inventory_item',
        write_only=True
    )

    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        source='location',
        write_only=True
    )

    class Meta:
        model = Allocation
        fields = [
            'id',
            'inventory_item',
            'location',
            'allocated_to',
            'allocation_date',
            'return_date',
            'status',
            'notes',
            'created_by',
            'inventory_id',
            'location_id',
        ]
        read_only_fields = [
            'id',
            'allocation_date',
            'created_by',
            'inventory_item',
            'location',
        ]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
