from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Vendor(models.Model):

    name = models.CharField(max_length=255, verbose_name='Vendor Name')
    contact_details = models.TextField(verbose_name='Contact Details')
    address = models.TextField(verbose_name='Address')
    vendor_code = models.CharField(max_length=50, unique=True, verbose_name='Vendor Code')
    on_time_delivery_rate = models.FloatField(default=0, verbose_name='On-Time Delivery Rate')
    quality_rating_avg = models.FloatField(default=0, verbose_name='Quality Rating Average')
    average_response_time = models.FloatField(default=0, verbose_name='Average Response Time')
    fulfillment_rate = models.FloatField(default=0, verbose_name='Fulfillment Rate')

    class Meta:
        managed = True 
        db_table = 'vendor'

class PurchaseOrder(models.Model):

    po_number = models.CharField(max_length=50, unique=True, verbose_name='PO Number')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Vendor')  # Foreign Key
    order_date = models.DateTimeField(verbose_name='Order Date')
    delivery_date = models.DateTimeField(verbose_name='Delivery Date')
    items = models.JSONField(verbose_name='Items')
    quantity = models.IntegerField(verbose_name='Quantity')
    status = models.CharField(max_length=50, verbose_name='Status')
    quality_rating = models.FloatField(default=0, blank=True, verbose_name='Quality Rating')
    issue_date = models.DateTimeField(verbose_name='Issue Date')
    acknowledgment_date = models.DateTimeField(null=True, blank=True, verbose_name='Acknowledgment Date')

    class Meta:
        managed = True 
        db_table = 'orders'
    
    def update_status(self):
        if self.acknowledgment_date:
            self.status = 'completed'

@receiver(pre_save, sender=PurchaseOrder)
def update_po_status(sender, instance, **kwargs):
    instance.update_status()

class HistoricalPerformance(models.Model):

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Vendor') # Foreign Key
    date = models.DateTimeField(verbose_name='Date')
    on_time_delivery_rate = models.FloatField(default=0, verbose_name='On-Time Delivery Rate')
    quality_rating_avg = models.FloatField(default=0, verbose_name='Quality Rating Average')
    average_response_time = models.FloatField(default=0, verbose_name='Average Response Time')
    fulfillment_rate = models.FloatField(default=0, verbose_name='Fulfillment Rate')

    class Meta:
        managed = True 
        db_table = 'performance'