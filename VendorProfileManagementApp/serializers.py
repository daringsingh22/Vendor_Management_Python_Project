from datetime import datetime
from rest_framework import serializers
from .models import VendorModel, PurchaseOrderModel, HistoricalPerformanceModel


# Serializer for Vendor model
class VendorModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = '__all__'
    

# Serializer for Purchase Order model
class PurchaseOrderModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderModel
        fields = '__all__'
    

    # validate order date <= delivery date
    def validate(self, data):
        current_date = datetime.now().date()
        delivery_date = data.get('delivery_date')
        if delivery_date and current_date and delivery_date < current_date:
            raise serializers.ValidationError("Delivery date cannot be less than order date!")

        return data

class HistoricalPerformanceModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformanceModel
        fields = '__all__'