from django.contrib import admin
from beermanagment.models import Bar, Reference, Stock, Order, OrderItem

admin.site.register([Bar, Reference, Stock, Order, OrderItem])
# Register your models here.
