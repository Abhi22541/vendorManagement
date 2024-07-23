from django.db import models
from datetime import timedelta
from django.db.models import Avg,F,Sum

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def update_on_time_delivery_rate(self):
        completed_orders = self.purchase_orders.filter(status='completed')
        if not completed_orders.exists():
            self.on_time_delivery_rate = 0.0
        else:
            on_time_deliveries = completed_orders.filter(delivery_date__lte=F('delivery_date')).count()
            self.on_time_delivery_rate = (on_time_deliveries / completed_orders.count()) * 100
        self.save()

    def update_quality_rating_avg(self):
        completed_orders = self.purchase_orders.filter(status='completed')
        self.quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0
        self.save()

    def update_average_response_time(self):
        acknowledged_orders = self.purchase_orders.filter(acknowledgment_date__isnull=False)
        if not acknowledged_orders.exists():
            self.average_response_time = 0.0
        else:
            total_response_time = acknowledged_orders.aggregate(total_response_time=Sum(F('acknowledgment_date') - F('issue_date')))['total_response_time'] or timedelta(0)
            self.average_response_time = total_response_time.total_seconds() / acknowledged_orders.count() / 3600  # Convert to hours
        self.save()

    def update_fulfillment_rate(self):
        total_orders = self.purchase_orders.count()
        if total_orders == 0:
            self.fulfillment_rate = 0.0
        else:
            fulfilled_orders = self.purchase_orders.filter(status='completed').count()
            self.fulfillment_rate = (fulfilled_orders / total_orders) * 100
        self.save()

    def update_performance_metrics(self):
        self.update_on_time_delivery_rate()
        self.update_quality_rating_avg()
        self.update_average_response_time()
        self.update_fulfillment_rate()

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, related_name='purchase_orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='historical_performances', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
