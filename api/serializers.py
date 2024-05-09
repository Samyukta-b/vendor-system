from rest_framework import serializers
from myapp.models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code']

class POSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    def validate(self, attrs):
        items_data = attrs.get('items', [])
        quantity = attrs.get('quantity', 0)
        order_date = attrs.get('order_date')
        delivery_date = attrs.get('delivery_date')

        if len(items_data) != quantity:
            raise serializers.ValidationError("The number of items and quantity do not match")

        if delivery_date <= order_date:
            raise serializers.ValidationError("The delivery date is before the order date")
        return attrs

class HPSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'

from datetime import datetime

class AckSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ['acknowledgment_date', 'issue_date']

    def validate(self, attrs):
        issue_date = self.instance.issue_date
        ack_date = attrs.get('acknowledgment_date')

        if issue_date is None:
            raise serializers.ValidationError("The issue date is not set for this purchase order")

        if ack_date and ack_date <= issue_date:
            raise serializers.ValidationError("The acknowledgment date is before the issue date")
        return attrs


class QualityRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ['quality_rating']

    def validate(self, attrs):
        quality_rating = attrs.get('quality_rating')
        if quality_rating is not None and (quality_rating < 1 or quality_rating > 5):
            raise serializers.ValidationError("Quality rating must be between 1 and 5.")
        return attrs