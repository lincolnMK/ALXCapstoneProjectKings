from rest_framework import serializers

from donorbuyer.serializers import DonorBuyerSerializer
from donorbuyer.models import DonorBuyer
from .models import Asset

class AssetSerializer(serializers.ModelSerializer):
    # Nested display
    donor_buyer = DonorBuyerSerializer(read_only=True)
    
    # Accept ID on input
    donor_buyer_id = serializers.PrimaryKeyRelatedField(
        source='donor_buyer',  # assign to donor_buyer ForeignKey
        queryset=DonorBuyer.objects.all(),
        write_only=True
    )

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_serial_number(self, value):
        if not value.strip():
            raise serializers.ValidationError("Serial number cannot be empty.")
        return value

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("Asset value must be positive.")
        return value