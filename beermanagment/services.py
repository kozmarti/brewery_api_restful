import logging
from django.core.exceptions import ObjectDoesNotExist
from beermanagment.models import Bar, Order, Reference, Stock

logger = logging.getLogger(__name__)


def get_full_and_non_full_bars() -> dict:
    bars_full_non_full = {
        'all_stocks': [],
        'miss_at_least_one': []
    }
    references = Reference.objects.all().values_list('id', flat=True)
    bars = Bar.objects.all()
    for bar in bars:
        if references == Stock.objects.filter(bar=bar).values_list('reference', flat=True):
            bars_full_non_full['all_stocks'].append(bar.id)
        else:
            bars_full_non_full['miss_at_least_one'].append(bar.id)
    return bars_full_non_full


def order_change_stock(order: Order):
    stocks_in_bar = Stock.objects.filter(bar=order.bar)
    if not stocks_in_bar:
        logger.error('There is no beer at all on stock in this empty bar!')
        return
    orderitems = order.items.all()
    for orderitem in orderitems:
        less_than_2_error_message = f'Stock for beer (id: {orderitem.reference.id}) is less than 2, refill needed!'
        no_beer_on_stock_error_message = f'There is no beer (id: {orderitem.reference.id}) on stock in this bar!'
        try:
            stock_for_reference_in_bar = stocks_in_bar.get(reference=orderitem.reference)
            if stock_for_reference_in_bar.stock >= orderitem.count:
                stock_for_reference_in_bar.stock -= orderitem.count
                stock_for_reference_in_bar.save()
                logger.info(f'Order (id: {orderitem.reference.id}) OK')
                if stock_for_reference_in_bar.stock < 2:
                    logger.warning(less_than_2_error_message)
            elif stock_for_reference_in_bar.stock:
                logger.error(f'Only {stock_for_reference_in_bar.stock} beer '
                             f'was in stock for beer (id: {orderitem.reference.id}, '
                             f'{orderitem.count - stock_for_reference_in_bar.stock} could not be sold to customer!')
                stock_for_reference_in_bar.stock = 0
                stock_for_reference_in_bar.save()
                logger.warning(less_than_2_error_message)
            else:
                logger.error(no_beer_on_stock_error_message)
        except ObjectDoesNotExist:
            logger.error(no_beer_on_stock_error_message)
