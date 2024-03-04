from django.urls import path
from .views import (
        VendorModelListCreateView, VendorModelListRetriveUpdateDestroy, 
        PurchaseOrderListCreateView, PurchaseOrderListRetriveUpdateDestroy,
        HistoricalListCreateView, # HistoricalListRetriveUpdateDestroy,
        performance_metric, acknowledge_order
    )


urlpatterns = [
    path('vendors/', VendorModelListCreateView.as_view(), name= 'vendor-post-get-view'),
    path('vendors/<uuid:vendor_code>/',VendorModelListRetriveUpdateDestroy.as_view(), name = 'vendor-get-put-delete-view'),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name= 'purchaseOrder-post-get-view'),
    path('purchase_orders/<str:po_number>/',PurchaseOrderListRetriveUpdateDestroy.as_view(), name = 'purchaseOrder-get-put-delete-view'),
    path('vendors/<str:vendor_code>/performance/',performance_metric, name= 'performance-metric'),
    path('purchase_orders/<str:po_number>/acknowledge/',acknowledge_order, name='acknowledge-order'),
    path('historical_performance/',HistoricalListCreateView.as_view(),name='historical-post-get-view')
]