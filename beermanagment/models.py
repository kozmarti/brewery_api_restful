from django.db import models


class Reference(models.Model):
    reference = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['reference']


class Bar(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Stock(models.Model):
    reference = models.ForeignKey("Reference", on_delete=models.CASCADE)
    bar = models.ForeignKey("Bar", on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f'in bar "{self.bar.name}" {self.stock} bottle of "{self.reference.name}" is on stock'

    class Meta:
        ordering = ['id']


class Order(models.Model):
    bar = models.ForeignKey("Bar", on_delete=models.CASCADE)

    # def __str__(self):
    #     return f'From bar "{self.bar.name}" beers ordered: {[i.reference.name for i in self.items.all()]} '

    class Meta:
        ordering = ['-id']


class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name='items', on_delete=models.CASCADE)
    reference = models.ForeignKey("Reference", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.count} bottle(s) of {self.reference.name} beer ordered'
