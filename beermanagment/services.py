from email import message
from tracemalloc import get_object_traceback
from beermanagment.models import Bar, Order, Reference, Stock
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

def get_full_and_non_full_bars() -> dict:
	bars = {
			'all_stocks' : [],
		    'miss_at_least_one': []
			}
	references = Reference.objects.all().values_list('id', flat=True)
	for bar in Bar.objects.all():
		if references == Stock.objects.filter(bar=bar).values_list('reference', flat=True):
			bars['all_stocks'].append(bar.id)
		else:
			bars['miss_at_least_one'].append(bar.id)
	return bars


def order_change_stock(order: Order):
	stocks_in_bar = Stock.objects.filter(bar=order.bar)
	if not stocks_in_bar:
		logger.error('There is no beer on stock at all in this bar!')
		return
	orderitems = order.items.all()
	for orderitem in orderitems:
		try:
			stock_for_reference_in_bar = stocks_in_bar.get(reference=orderitem.reference)
			if stock_for_reference_in_bar.stock >= orderitem.count:
				stock_for_reference_in_bar.stock -= orderitem.count
				stock_for_reference_in_bar.save()
				logger.info('Order OK')
				if stock_for_reference_in_bar.stock < 2:
					logger.info('Stock for beer (id:' + str(orderitem.reference) + ') is less than 2, refill needed!')
			elif stock_for_reference_in_bar:
				logger.error('only ' + str(stock_for_reference_in_bar.stock) +
										   'beer was in stock' + str(orderitem.count - stock_for_reference_in_bar.stock) +
										   'could not be sold to customer!')
				stock_for_reference_in_bar.stock = 0
				stock_for_reference_in_bar.save()
			else:
				message_no_beer = 'There is no this beer (id: ' + str(orderitem.reference) + ') on stock in this bar!'
				logger.error(message_no_beer)
		except ObjectDoesNotExist:
			logger.error(message_no_beer)

