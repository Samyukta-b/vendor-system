from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from myapp.models import Vendor, PurchaseOrder
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class VendorViewCreateAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'Contact Info',
            'address': 'Test Address',
            'vendor_code': '123'
        }

    def test_create_vendor(self): # PASS
        url = reverse('api:api-vendors-list')
        headers = {'Authorization': f'Token {self.token.key}'}
        response = self.client.post(url, self.vendor_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'Test Vendor')

class VendorDetailsAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact Info', address='Test Address', vendor_code='123')

    def test_retrieve_vendor(self):
        url = reverse('api:api-vendor-details', kwargs={'vendor_id': self.vendor.id})
        headers = {'Authorization': f'Token {self.token.key}'}
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Vendor')

class POViewCreateAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact Info', address='Test Address', vendor_code='123')
        self.po_data = {
            'po_number': '123456',
            'vendor': self.vendor.id,
            'order_date': timezone.now(),
            'delivery_date': timezone.now() + timezone.timedelta(days=2),
            'items': [{'name': 'Item 1', 'price': 20.00}, {'name': 'Item 2', 'price': 30.00}],
            'quantity': 2,
            'status': 'pending',
            'issue_date': timezone.now(),
        }

    def test_create_purchase_order(self):
        url = reverse('api:api-purchase-orders-list')
        headers = {'Authorization': f'Token {self.token.key}'}
        response = self.client.post(url, self.po_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(PurchaseOrder.objects.get().po_number, '123456')

class PODetailsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)

        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact Info', address='Test Address', vendor_code='123')
        self.purchase_order = PurchaseOrder.objects.create(po_number='123456', vendor=self.vendor, order_date=timezone.now(), delivery_date=timezone.now() + timezone.timedelta(days=2), items=[{"name": "Product A"}, {"name": "Product B"},], quantity=2, status='pending', issue_date=timezone.now())

    def test_retrieve_purchase_order(self):
        url = reverse('api:api-po-details', kwargs={'po_id': self.purchase_order.id})
        headers = {'Authorization': f'Token {self.token.key}'}
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], '123456')
