from rest_framework import serializers
from .models import Asset

class AssetSerializer(serializers.ModelSerializer):

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
