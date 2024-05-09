from django.test import TestCase
from datetime import datetime, timedelta
from myapp.models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Test Contact Details',
            address='Test Address',
            vendor_code='V001',
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=98.0
        )

    def test_vendor_creation(self):
        self.assertEqual(self.vendor.name, 'Test Vendor')

class PurchaseOrderModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Test Contact Details',
            address='Test Address',
            vendor_code='V001',
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=98.0
        )

    def test_order_creation(self):
        order = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=datetime.now(),
            delivery_date=datetime.now() + timedelta(days=7),
            items=['Item 1', 'Item 2'],
            quantity=10,
            status='pending',
            issue_date=datetime.now(),
            acknowledgment_date=None
        )
        self.assertEqual(order.po_number, 'PO001')

    def test_order_status_update(self):
        order = PurchaseOrder.objects.create(
            po_number='PO002',
            vendor=self.vendor,
            order_date=datetime.now(),
            delivery_date=datetime.now() + timedelta(days=7),
            items=['Item 1', 'Item 2'],
            quantity=10,
            status='pending',
            issue_date=datetime.now(),
            acknowledgment_date=datetime.now() 
        )
        
        order.refresh_from_db() 
        self.assertEqual(order.status, 'completed')

class HistoricalPerformanceModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Test Contact Details',
            address='Test Address',
            vendor_code='V001',
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=98.0
        )

    def test_historical_performance_creation(self):
        performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date=datetime.now(),
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=98.0
        )
        self.assertEqual(performance.vendor.name, 'Test Vendor')
