from celery import shared_task
from django.utils import timezone
from .models import Order

@shared_task
def cancel_expired_orders():
    one_day_ago = timezone.now() - timezone.timedelta(days=1)
    orders_to_cancel = Order.objects.filter(
        status=Order.Statuses.RESERVED,
        reserve_time__lt=one_day_ago
    )
    for order in orders_to_cancel:
        order.status = Order.Statuses.RETURNED
        order.save()
    return f"Canceled {orders_to_cancel.count()} expired orders"