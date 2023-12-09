from django.db import models
from vendor_profile.models import Vendor


class OrderItems(models.Model):
	name = models.TextField()

PO_STATUS = (
	("pending", "pending"),
	("completed", "completed"),
	("canceled", "cancelled"),
)

class PurchaseOrder(models.Model):
	po_number = models.CharField(max_length=30, unique=True, editable=False)
	vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
	order_date = models.DateTimeField(auto_now_add=True)
	delivery_date = models.DateTimeField()  # Expected delivery date
	actual_delivery_date = models.DateTimeField(null=True, blank=True)
	items = models.JSONField()
	quantity = models.IntegerField()
	status = models.CharField(max_length=20,choices=PO_STATUS)
	quality_rating = models.FloatField(null=True, blank=True)
	issue_date = models.DateTimeField(auto_now_add=True)
	acknowledgment_date = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return str(self.id)