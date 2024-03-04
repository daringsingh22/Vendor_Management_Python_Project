from django.shortcuts import render
from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import VendorModelSerializers, PurchaseOrderModelSerializers, HistoricalPerformanceModelSerializers
from .models import VendorModel, PurchaseOrderModel, HistoricalPerformanceModel
from .signals import avg_response_time

# views for Vendor model.

# post, get for vendor details
class VendorModelListCreateView(generics.ListCreateAPIView):
    queryset = VendorModel.objects.all()
    serializer_class = VendorModelSerializers
    permission_classes = [IsAuthenticated]


# get , put, delete for individual vendor details
class VendorModelListRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = VendorModel.objects.all()
    serializer_class = VendorModelSerializers
    lookup_field = 'vendor_code'
    permission_classes = [IsAuthenticated]



# views for Purchase Order model.

# post, get for purchase order details
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrderModel.objects.all()
    serializer_class = PurchaseOrderModelSerializers
    permission_classes = [IsAuthenticated]


# get , put, delete for individual purchase order
class PurchaseOrderListRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrderModel.objects.all()
    serializer_class = PurchaseOrderModelSerializers
    lookup_field = 'po_number'
    permission_classes = [IsAuthenticated]


class HistoricalListCreateView(generics.ListCreateAPIView):
    queryset = HistoricalPerformanceModel.objects.all()
    serializer_class = HistoricalPerformanceModelSerializers
    permission_classes = [IsAuthenticated]


# get , put, delete for individual vendor historical performance
# class HistoricalListRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = HistoricalPerformanceModel.objects.all()
#     serializer_class = HistoricalPerformanceModelSerializers
#     lookup_field = 'id'
#     permission_classes = [IsAuthenticated]



# view for to calculate performance metric
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def performance_metric(request, vendor_code):
    try:
        if not VendorModel.objects.filter(vendor_code = vendor_code).exists():
            return Response({'Error': 'Vendor not found'})
        
        vendor_obj = VendorModel.objects.get(vendor_code = vendor_code)

        performance_result = {
            "on time delivery": vendor_obj.on_time_delivery_rate,
            "quality_rating_avg": vendor_obj.quality_rating_avg,
            "average_response_time": vendor_obj.average_response_time,
            "fulfillment_rate": vendor_obj.fulfillment_rate
        }
        
        return Response(performance_result)
    
    except Exception as exe:
        print('Error in performance_metric()', exe)


# function to update acknowledgment date
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_order(request, po_number):
    try:
        if not PurchaseOrderModel.objects.filter(po_number = po_number).exists():
            return Response({'Error': 'Purchase Order number not found'})

        # updating acknowledgement date to db
        po_order_obj = PurchaseOrderModel.objects.get(po_number = po_number)
        po_order_obj.acknowledgment_date = datetime.now()
        po_order_obj.save()

        vendor_obj = PurchaseOrderModel.objects.get(po_number = po_number).vendor

        # triggering signal to calculate avg response time
        result = avg_response_time.send(sender=PurchaseOrderModel, instance = vendor_obj) # output will be in list of tuples

        if result:
            return Response({'average_response_time':result[0][1]})
        else:
            return Response({'Error occured'})
        
    except Exception as exe:
        print('Error in acknowledge_order(): ', exe)

    