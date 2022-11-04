from django.db.models import signals
from django.dispatch import receiver
from .models import Stock
import logging

logger = logging.getLogger(__name__)


@receiver(signals.post_save, sender=Stock)
def is_stock_less_than_2(sender, instance, **kwargs):
    if instance.stock < 2:
        logger.warning(f'There is only {instance.stock} beer (id : {instance.reference.id}) on stock , refill needed.')