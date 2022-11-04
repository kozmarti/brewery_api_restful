from django.db import models


class Reference(models.Model):
    reference = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['reference']


class Bar(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['id']


class Stock(models.Model):
    reference = models.ForeignKey("Reference", on_delete=models.CASCADE)
    bar = models.ForeignKey("Bar", on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()

    class Meta:
        ordering = ['id']


class Order(models.Model):
    bar = models.ForeignKey("Bar", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name='items', on_delete=models.CASCADE)
    reference = models.ForeignKey("Reference", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
