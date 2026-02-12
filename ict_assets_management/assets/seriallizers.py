from rest_framework import serializers
from .models import Asset
from donorbuyer.models import Donor_Buyer
from donorbuyer.serializers import DonorBuyerSerializer


class AssetSerializer(serializers.ModelSerializer):
    donor_buyer = DonorBuyerSerializer(read_only=True)
    donor_buyer_id = serializers.PrimaryKeyRelatedField(
        queryset=Donor_Buyer.objects.all(),
        source='donor_buyer',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Asset
        fields = '__all__'
