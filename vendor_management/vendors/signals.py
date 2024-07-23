from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics_on_save(sender, instance, **kwargs):
    instance.vendor.update_performance_metrics()

@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_metrics_on_delete(sender, instance, **kwargs):
    instance.vendor.update_performance_metrics()
