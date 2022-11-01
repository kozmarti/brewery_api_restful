import logging
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from beermanagment.models import Bar, Order, Stock

logger = logging.getLogger(__name__)


def get_full_and_non_full_bars(bars: QuerySet[Bar], references: list) -> dict:
    bars_full_non_full = {
        'all_stocks': [],
        'miss_at_least_one': []
    }
    for bar in bars:
        if references == Stock.objects.filter(bar=bar).values_list('reference', flat=True):
            bars_full_non_full['all_stocks'].append(bar.id)
        else:
            bars_full_non_full['miss_at_least_one'].append(bar.id)
    return bars_full_non_full


def order_change_stock(order: Order) -> str:
    stocks_in_bar = Stock.objects.filter(bar=order.bar)
    messages = []
    if not stocks_in_bar:
        no_stock_message = 'There is no beer at all on stock in this empty bar! '
        logger.error(no_stock_message)
        return no_stock_message
    orderitems = order.items.all()
    for orderitem in orderitems:
        less_than_2_error_message = f'Stock for beer (id: {orderitem.reference.id}) is less than 2, refill needed! '
        no_beer_on_stock_error_message = f'There is no beer (id: {orderitem.reference.id}) on stock in this bar! '
        try:
            stock_for_reference_in_bar = stocks_in_bar.get(reference=orderitem.reference)
            if stock_for_reference_in_bar.stock >= orderitem.count:
                stock_for_reference_in_bar.stock -= orderitem.count
                stock_for_reference_in_bar.save()
                messages.append(f'Order (beer id: {orderitem.reference.id}) OK ')
                if stock_for_reference_in_bar.stock < 2:
                    messages.append(less_than_2_error_message)
            elif stock_for_reference_in_bar.stock:
                messages.append(f'Only {stock_for_reference_in_bar.stock} beer'
                                f' was in stock for beer (id: '
                                f'{orderitem.reference.id}), '
                                f'{orderitem.count - stock_for_reference_in_bar.stock}'
                                f' could not be sold to customer! ')
                stock_for_reference_in_bar.stock = 0
                stock_for_reference_in_bar.save()
                messages.append(less_than_2_error_message)
            else:
                messages.append(no_beer_on_stock_error_message)
        except ObjectDoesNotExist:
            messages.append(no_beer_on_stock_error_message)
    logger.error(messages)
    return messages
