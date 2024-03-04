from django.contrib import admin
from .models import VendorModel, PurchaseOrderModel, HistoricalPerformanceModel

# Register your models here.
admin.site.register(VendorModel)
admin.site.register(PurchaseOrderModel)
admin.site.register(HistoricalPerformanceModel)