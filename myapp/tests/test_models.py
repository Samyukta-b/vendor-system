from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from myapp.models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="test@example.com",
                                            address="123 Test St", vendor_code="TEST123")

    def test_vendor_creation(self):
        self.assertEqual(self.vendor.name, "Test Vendor")
        # Add more assertions to test other fields and methods in Vendor model

class PurchaseOrderModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="test@example.com",
                                            address="123 Test St", vendor_code="TEST123")
        self.order = PurchaseOrder.objects.create(po_number="PO123", vendor=self.vendor,
                                                  order_date="2024-05-09T12:00:00Z",
                                                  delivery_date="2024-05-16T12:00:00Z",
                                                  items=[], quantity=1, status="pending",
                                                  issue_date="2024-05-09T12:00:00Z")

    def test_order_creation(self):
        self.assertEqual(self.order.po_number, "PO123")
        # Add more assertions to test other fields and methods in PurchaseOrder model

class HistoricalPerformanceModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='1234567890', address='Test Address', vendor_code='TV001')
        self.hp = HistoricalPerformance.objects.create(vendor=self.vendor, date='2024-05-01', on_time_delivery_rate=90, quality_rating_avg=4.5, average_response_time=2.5, fulfillment_rate=95)

    def test_historical_performance_creation(self):
        self.assertEqual(self.hp.vendor.name, 'Test Vendor')
        self.assertEqual(self.hp.date, '2024-05-01')
        self.assertEqual(self.hp.on_time_delivery_rate, 90)
        self.assertEqual(self.hp.quality_rating_avg, 4.5)
        self.assertEqual(self.hp.average_response_time, 2.5)
        self.assertEqual(self.hp.fulfillment_rate, 95)
