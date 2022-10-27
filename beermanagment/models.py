from django.db import models


class Reference(models.Model):
	reference = models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=200, blank=True)

	class Meta:
		ordering = ['reference']


class Bar(models.Model):
	name = models.CharField(max_length=30)


class Stock(models.Model):
	reference = models.ForeignKey("Reference", on_delete=models.CASCADE)
	bar = models.ForeignKey("Bar", on_delete=models.CASCADE)
	stock = models.PositiveIntegerField()


class Order(models.Model):
	bar = models.ForeignKey("Bar", on_delete=models.CASCADE)


class OrderItem(models.Model):
	order = models.ForeignKey("Order", on_delete=models.CASCADE)
	reference = models.ForeignKey("Reference", on_delete=models.CASCADE)
	count = models.PositiveIntegerField()