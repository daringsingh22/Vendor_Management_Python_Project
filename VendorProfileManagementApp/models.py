import uuid, random
from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
# Vendor model
class VendorModel(models.Model):
    vendor_code = models.CharField(primary_key=True,max_length=40, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

# to generate unique number
def generate_unique_number():
    while True:
        number = random.randint(10000000, 99999999)
        if not PurchaseOrderModel.objects.filter(po_number=number).exists():
            po_number = str(number)
            return po_number


# Purchase Order Model
class PurchaseOrderModel(models.Model):
    po_number = models.CharField(max_length=10,default=generate_unique_number, primary_key=True, editable=False)
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    items = models.JSONField()
    quantity = models.IntegerField(default=1)

    status = models.CharField(
            max_length=20, 
            choices=[
                ('pending', 'Pending'),
                ('completed', 'Completed'),
                ('cancelled', 'Cancelled'),
            ],
            default= 'pending'
        )
    
    
    quality_rating = models.FloatField(
            null=True,
            validators=[MinValueValidator(1.0),MaxValueValidator(10.0)],
        )
    
    delivery_date = models.DateField()

    delivery_status = models.CharField(
            max_length=1,
            choices=[
                ('Y','On Time'),
                ('N','Delayed')
            ],
            null=True
        )
    
    issue_date = models.DateTimeField(default= datetime.now())
    acknowledgment_date = models.DateTimeField(null=True)


# Historical Performance Model
class HistoricalPerformanceModel(models.Model):
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)