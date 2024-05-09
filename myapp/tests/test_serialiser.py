from django.test import TestCase
from django.utils import timezone
from myapp.models import Vendor, PurchaseOrder, HistoricalPerformance
from api.serializers import POSerializer, HPSerializer, AckSerializer, QualityRateSerializer

class PurchaseOrderSerializerTest(TestCase):

    def setUp(self): 
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact Info', address='Test Address', vendor_code='123')
        self.data = {
            'po_number': '123456',
            'vendor': self.vendor.id,
            'order_date': "2024-05-05T10:00:00",
            'delivery_date': "2024-05-07T10:00:00" ,
            'items': [{'name': 'Item 1', 'price': 20.00}, {'name': 'Item 2', 'price': 30.00}],
            'quantity': 2,
            'status': 'pending',
            'issue_date': "2024-05-05T10:00:00",
        }

    def test_purchase_order_serializer_valid(self): # PASS
        serializer = POSerializer(data=self.data)
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())


    def test_purchase_order_serializer_invalid_item_quantity(self): # PAS
        self.data['quantity'] = 5
        serializer = POSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_purchase_order_serializer_invalid_delivery_date(self):
        self.data['delivery_date'] = "2024-05-03T10:00:00"
        serializer = POSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

class HistoricalPerformanceSerializerTest(TestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact Info', address='Test Address', vendor_code='123')
        self.data = {
            'vendor': self.vendor.id,
            'date': timezone.now(),
            'on_time_delivery_rate': 95.5,
            'quality_rating_avg': 4.5,
            'average_response_time': 24,
            'fulfillment_rate': 98.2,
        }

    def test_historical_performance_serializer_valid(self):
        serializer = HPSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

class AcknowledgmentSerializerTest(TestCase):

    def setUp(self):
        self.purchase_order = PurchaseOrder.objects.create(po_number='123456', vendor=Vendor.objects.create(name='Test Vendor', contact_details='Contact Info', address='Test Address', vendor_code='123'), 
        order_date=timezone.now(), delivery_date=timezone.now() + timezone.timedelta(days=7), items=[{"name": "Product A"}, {"name": "Product B"}, {"name": "Product C"}], quantity=3, status='pending', issue_date=timezone.now())

    def test_ack_serializer_valid(self):
        data = {'acknowledgment_date': timezone.now() + timezone.timedelta(days=1), 'issue_date': self.purchase_order.issue_date}
        serializer = AckSerializer(instance=self.purchase_order, data=data)
        self.assertTrue(serializer.is_valid())

    def test_ack_serializer_invalid_ack_date_before_issue_date(self):
        data = {'acknowledgment_date': timezone.now() - timezone.timedelta(days=1), 'issue_date': self.purchase_order.issue_date}
        serializer = AckSerializer(instance=self.purchase_order, data=data)
        self.assertFalse(serializer.is_valid())

class QualityRatingSerializerTest(TestCase):

    def setUp(self):
        self.purchase_order = PurchaseOrder.objects.create(po_number='123456', vendor=Vendor.objects.create(name='Test Vendor', contact_details='Contact Info', address='Test Address', vendor_code='123'), order_date=timezone.now(), delivery_date=timezone.now() + timezone.timedelta(days=7), items=[], quantity=10, status='pending', issue_date=timezone.now())

    def test_quality_rate_serializer_valid(self):
        data = {'quality_rating': 4}
        serializer = QualityRateSerializer(instance=self.purchase_order, data=data)
        self.assertTrue(serializer.is_valid())

    def test_quality_rate_serializer_invalid_rating_out_of_range(self):
        data = {'quality_rating': 6}
        serializer = QualityRateSerializer(instance=self.purchase_order, data=data)
        self.assertFalse(serializer.is_valid())

