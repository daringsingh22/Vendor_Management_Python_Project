from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import PurchaseOrderModel, VendorModel
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

#Create your tests here.
class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # self.vendor_code = None

        # Creating a test user
        self.user = User.objects.create_user(username='admin', password='1234')

        # Creating token for test user
        self.token = Token.objects.create(user= self.user)

        # Inserting token to client's header for authenticated user
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")


    # function to test vendor api
    def test_vendor_api_post(self):

        print('\n<------- Testing API for Vendor details creation ------->\n')

        self.vendor_data = { "name":"Blue Dart",
                        "contact_details":"123457890",
                        "address":"Bangalore"
                    }
        self.vendor_response = self.client.post(reverse('vendor-post-get-view'), self.vendor_data, format='json')
        self.assertEqual(self.vendor_response.status_code, status.HTTP_201_CREATED)

        print('Record created for Vendor : ',self.vendor_response.data['name'])
        print(self.vendor_response.data)



        print('\n<------- Testing API for Purchase order details creation ------->\n')

        purchase_order_data = {
                            "vendor":self.vendor_response.data['vendor_code'],
                            "items":{
                                        "product":"charger"
                                    },
                            "quantity":2,
                            "delivery_date":"2023-12-13"
                        }
        self.purchase_reponse = self.client.post(reverse('purchaseOrder-post-get-view'), purchase_order_data, format='json')
        self.assertEqual(self.purchase_reponse.status_code, status.HTTP_201_CREATED)

        print('Purcase order created for Vendor : ',self.purchase_reponse.data['po_number'])
        print(self.purchase_reponse.data)
        


        print('\n<------- Testing API for acknowledgement  ------->\n')

        self.ack_response = self.client.post(reverse('acknowledge-order',
                                                     args=[self.purchase_reponse.data['po_number']]))
        self.assertEqual(self.ack_response.status_code, status.HTTP_200_OK)
        print('Acknowledge the order : ',self.ack_response.data)



        print('\n<------- Testing API for calculating metrics ------->\n')

        update_data = {
                            "status": "completed",
                            "quality_rating": 8.8
                        }
        
        self.metrix_response = self.client.patch(reverse('purchaseOrder-get-put-delete-view', 
                                            args=[self.purchase_reponse.data['po_number']]),update_data, format='json')
        self.assertEqual(self.metrix_response.status_code, status.HTTP_200_OK)
        print('Metric updated for order no : ',self.metrix_response.data['po_number'])
        print(self.metrix_response.data)



        print('\n<------- Display performance metrix API for vendor ------->\n')
        
        self.per_met_response = self.client.get(reverse('performance-metric', args=[self.vendor_response.data['vendor_code']]))
        
        self.assertEqual(self.per_met_response.status_code, status.HTTP_200_OK)
        print('Performance metrix for Vendor ',self.vendor_response.data['name'])
        print(self.per_met_response.data)
