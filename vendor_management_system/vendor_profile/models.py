from django.db import models

class Vendor(models.Model):
	name = models.CharField(max_length=255)
	contact_details = models.TextField()
	address = models.TextField()
	vendor_code = models.CharField(max_length=30, unique=True)
	on_time_delivery_rate = models.FloatField(default=0)
	quality_rating_avg = models.FloatField(default=0)
	average_response_time = models.FloatField(default=0)
	fulfillment_rate = models.FloatField(default=0)

	def __str__(self):
		return self.name

class HistoricalPerformance(models.Model):
	vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
	date = models.DateTimeField()
	on_time_delivery_rate = models.FloatField(default=0)
	quality_rating_avg = models.FloatField(default=0)
	average_response_time = models.FloatField(null=True)
	fulfillment_rate = models.FloatField(null=True)

	def __str__(self):
		return self.name
