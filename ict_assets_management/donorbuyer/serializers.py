from rest_framework import serializers
from .models import DonorBuyer


class DonorBuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = DonorBuyer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_phone_number(self, value):
        if value and not value.replace('+', '').replace('-', '').isdigit():
            raise serializers.ValidationError("Phone number must contain only digits, + or -.")
        return value

    def validate(self, data):
        donor_type = data.get('type')
        email = data.get('email')

        if donor_type == 'buyer' and not email:
            raise serializers.ValidationError({
                "email": "Email is required when creating a buyer."
            })
        return data
