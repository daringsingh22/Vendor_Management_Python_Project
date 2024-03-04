from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from django.core.exceptions import ValidationError
from django.db.models import F, ExpressionWrapper, Avg, DurationField, Q, Max
from rest_framework.response import Response
from .models import PurchaseOrderModel, VendorModel, HistoricalPerformanceModel
from datetime  import datetime


avg_response_time = Signal()

def calculate_avg_response_time(sender, instance, **kwargs):
    try:
        vendor_id = instance.vendor_code
        query_result = PurchaseOrderModel.objects.filter(
            vendor__vendor_code= vendor_id, 
            acknowledgment_date__isnull = False
            )
        # print(query_result.count(), query_result)
        
        time_diff_expression = ExpressionWrapper(
            F('acknowledgment_date')-F('issue_date'),output_field=DurationField()
            )
        
        average_time_difference = query_result.aggregate(
            avg_time = Avg(time_diff_expression)
            )['avg_time'].total_seconds()
        
        average_time_difference = round(average_time_difference, 2)

        # print(round(average_time_difference, 2), type(average_time_difference))
        vendor_obj = VendorModel.objects.get(vendor_code = vendor_id)
        vendor_obj.average_response_time = average_time_difference
        vendor_obj.save()

        return average_time_difference
    
    except Exception as exe:
        print('Error in calculate_avg_response_time(): ',exe)
        return False

avg_response_time.connect(calculate_avg_response_time, sender= PurchaseOrderModel)


def cal_on_time_delivery_rate(instance):
    try:
        current_date = datetime.now().date()

        # to update the whether order was delivered on time or not when status changed to "completed"
        if current_date <= instance.delivery_date:
            instance.delivery_status = 'Y'
            instance.save()
            # print('updated')
        else:
            instance.delivery_status = 'N'
            instance.save()
            # print('updated')

        # result for completed orders
        order_query_result = PurchaseOrderModel.objects.filter(
                                Q(vendor = instance.vendor) & Q(status = "completed")
                                )

        # result for ontime delivery status
        ontime_delivery_result = PurchaseOrderModel.objects.filter(
                                    Q(vendor= instance.vendor) & Q(delivery_status = 'Y')
                                    )
        
        if order_query_result.exists() and ontime_delivery_result.exists():
            ontime_delivery_rate = format((ontime_delivery_result.count() / order_query_result.count()) * 100, '.2f')
            vendor_result = VendorModel.objects.get(vendor_code = instance.vendor.vendor_code)
            vendor_result.on_time_delivery_rate = ontime_delivery_rate
            vendor_result.save()

    except Exception as exe:
        print('Error in cal_on_time_delivery_rate() ', exe)
    

def cal_quality_rating_avg(instance):
    try:
        order_query_result = PurchaseOrderModel.objects.filter(
                                Q(vendor = instance.vendor) & Q(status= 'completed') & ~Q(quality_rating= None)
                                )
        
        if order_query_result.exists():
            # print('updated quality rating')
            quality_rating_average = order_query_result.aggregate(rating_avg = Avg('quality_rating'))['rating_avg']
            vendor_query_result = VendorModel.objects.get(vendor_code = instance.vendor.vendor_code)
            vendor_query_result.quality_rating_avg = quality_rating_average
            vendor_query_result.save()

    except Exception as exe:
        print('Error in cal_quality_rating_avg() ', exe)


def cal_fulfilment_rate(instance):
    try:
        order_query_result = PurchaseOrderModel.objects.filter(vendor= instance.vendor)
        completed_query_result = PurchaseOrderModel.objects.filter(vendor= instance.vendor, status= 'completed')

        if order_query_result.exists() and completed_query_result.exists():
            fulfillment_rate = format((completed_query_result.count() / order_query_result.count())*100,'.2f')
            vendor_query_result = VendorModel.objects.get(vendor_code = instance.vendor.vendor_code)
            vendor_query_result.fulfillment_rate = fulfillment_rate
            vendor_query_result.save()

    except Exception as exe:
        print('Error in cal_fulfilment_rate() ', exe)
    

def historical_performance(instance):
    try:
        vendor_result = VendorModel.objects.get(vendor_code = instance.vendor.vendor_code)
        current_date = datetime.now().date()

        if HistoricalPerformanceModel.objects.filter(vendor= instance.vendor.vendor_code).exists():
            latest_performance_date = HistoricalPerformanceModel.objects.filter(
                                        vendor = instance.vendor
                                        ).aggregate(latest_date = Max('date'))['latest_date']
            print('latest date ',latest_performance_date)
            if latest_performance_date != current_date:
                HistoricalPerformanceModel.objects.create(
                    vendor= instance.vendor,
                    on_time_delivery_rate= vendor_result.on_time_delivery_rate,
                    quality_rating_avg= vendor_result.quality_rating_avg,
                    average_response_time= vendor_result.average_response_time,
                    fulfillment_rate= vendor_result.fulfillment_rate
                    )
                
        else:
            HistoricalPerformanceModel.objects.create(
                    vendor= instance.vendor,
                    on_time_delivery_rate= vendor_result.on_time_delivery_rate,
                    quality_rating_avg= vendor_result.quality_rating_avg,
                    average_response_time= vendor_result.average_response_time,
                    fulfillment_rate= vendor_result.fulfillment_rate
                    )
    except Exception as exe:
        print('Error in historical_performance() ', exe)



# Django signal function to calculate metric like On-Time Delivery Rate, Quality Rating Average and 
# Fulfilment Rate whenever status changes to 'complete'
@receiver(post_save, sender = PurchaseOrderModel)
def cal_performance_metric(sender, instance, created, **kwargs):
    
    if instance.status == 'completed' and instance._state.adding is False:
        # print('inside cal_performance_metric')
        post_save.disconnect(cal_performance_metric, sender=PurchaseOrderModel)

        cal_on_time_delivery_rate(instance)
        cal_quality_rating_avg(instance)
        cal_fulfilment_rate(instance)

        historical_performance(instance)
        post_save.connect(cal_performance_metric, sender=PurchaseOrderModel)