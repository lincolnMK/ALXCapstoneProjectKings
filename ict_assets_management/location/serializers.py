from rest_framework import serializers
from .models import Location

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Location name cannot be empty.")
        return value
