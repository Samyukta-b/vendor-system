from myapp.models import PurchaseOrder, Vendor, HistoricalPerformance
from datetime import timedelta
from django.utils import timezone

class PerformanceMetrics:

    def get_all_metrics(self, vendor_id):
        vendor = Vendor.objects.get(id=vendor_id)
        if not vendor:
            return {"message": "Vendor not found with specified ID"}
        
        data = {
            "vendor": vendor_id,
            "date":timezone.now(),
            "on_time_delivery_rate (%)": self.on_time_delivery_rate(vendor),
            "quality_rating_average (out of 5)": self.quality_rating_average(vendor),
            "average_response_time (in hours)": self.average_response_time(vendor),
            "fulfilment_rate (%)": self.fulfillment_rate(vendor)
        }        
        self.update_vendor_fields(vendor)        
        return data

    def on_time_delivery_rate(self, vendor):
        orders = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
        if not orders:
            # Vendor does not have any completed purchase orders
            return 0
        completed_orders = orders.count()                    
        on_time_delivered_orders = 0
        for order in orders:
            order_date = order.order_date
            exp_delivery_date = order.delivery_date
            # The actual delivery date is one week from the order date
            actual_delivery_date = order_date + timedelta(days=7)
            if actual_delivery_date <= exp_delivery_date:
                on_time_delivered_orders += 1
        rate = on_time_delivered_orders / completed_orders * 100
        rate = round(rate, 2)
        return rate
        
    def quality_rating_average(self, vendor):
        orders = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
        if not orders:
            # Vendor does not have any completed purchase order
            return 0
        total_rate = 0
        count = 0
        for order in orders:
            if order.quality_rating is not None:
                quality_rate = order.quality_rating
                total_rate += quality_rate
                count += 1
        if count == 0:
            return 0    # No completed orders with quality ratings found
        avg_quality_rate = total_rate / count
        avg_quality_rate = round(avg_quality_rate, 2)
        return avg_quality_rate

    def average_response_time(self, vendor):
        orders = PurchaseOrder.objects.filter(vendor=vendor)
        total_seconds = 0
        count = 0
        for order in orders:
            issue = order.issue_date
            acknowledgement = order.acknowledgment_date
            if issue and acknowledgement:
                response = (acknowledgement - issue).total_seconds()                
                total_seconds += response
                count += 1
        if count == 0:
            return 0    # No orders with response time data found
        avg_response_seconds = total_seconds / count
        avg_response_rate = avg_response_seconds / 3600  
        avg_response_rate = round(avg_response_rate, 2)
        return avg_response_rate 

    def fulfillment_rate(self, vendor):
        orders = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
        if not orders:
            # Vendor does not have any completed purchase orders
            return 0
        completed_orders_count = orders.count()
        all_orders_count = PurchaseOrder.objects.filter(vendor=vendor).count()        
        f_rate = completed_orders_count / all_orders_count * 100
        f_rate = round(f_rate, 2)
        return f_rate
    
    def update_vendor_fields(self, vendor):
        new_on_time_delivery_rate = self.on_time_delivery_rate(vendor)
        new_quality_rating_avg = self.quality_rating_average(vendor)
        new_average_response_time = self.average_response_time(vendor)
        new_fulfillment_rate = self.fulfillment_rate(vendor)

        if new_on_time_delivery_rate != vendor.on_time_delivery_rate \
                or new_quality_rating_avg != vendor.quality_rating_avg \
                or new_average_response_time != vendor.average_response_time \
                or new_fulfillment_rate != vendor.fulfillment_rate:

            vendor.on_time_delivery_rate = new_on_time_delivery_rate
            vendor.quality_rating_avg = new_quality_rating_avg
            vendor.average_response_time = new_average_response_time
            vendor.fulfillment_rate = new_fulfillment_rate
            vendor.save()

            # Create a historical record only if there's new data to store
            historical_record = HistoricalPerformance.objects.create(
                vendor=vendor,
                on_time_delivery_rate=new_on_time_delivery_rate,
                quality_rating_avg=new_quality_rating_avg,
                average_response_time=new_average_response_time,
                fulfillment_rate=new_fulfillment_rate,
                date=timezone.now()
            )
            historical_record.save()
